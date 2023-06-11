import os
import glob
import oyaml
import pandas
import pickle
import subprocess

from fastapi import UploadFile

from define import define_feast_yaml, make_features_list, __mapping_feast_type
from _constant.feast_global import *
from _constant.feast_template.path import *
from _constant.feast_template.define import *

def __write_file_contents(file_path: str, contents: str):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(contents)


def __write_yaml_contents(file_path: str, contents: dict):
    with open(file_path, "w", encoding="utf-8") as yaml_file:
        oyaml.dump(yaml_file, contents)
    

def make_feast_init_files(workspace_id: int):
    ws_name = get_ws_name(workspace_id)
    ws_init_file = get_ws_feast_init_file(workspace_id)
    ws_config_file = get_ws_feast_config_file(workspace_id)
    __write_file_contents(ws_init_file, '')
    feast_yaml = define_feast_yaml(
        project=ws_name,
        registry=ws_name,
        provider='local',
        offline_type=FILE_TYPE,
        online_type=REDIS_TYPE
    )
    __write_yaml_contents(ws_config_file, feast_yaml)
    return ws_name


def __is_parquet(filename: str):
    _, ext = os.path.splitext(filename)
    return ext.lower() == '.parquet'


async def save_parquet_file(workspace_id: int, project_id: int, dataset_id: int, parquet_file: UploadFile):
    if not __is_parquet(filename=parquet_file.filename):
        return

    ds_parquet_path = get_base_parquet_path(workspace_id, project_id, dataset_id)
    try:
        with open(ds_parquet_path, 'wb') as f:
            f.write(await parquet_file.read())
    except Exception as e:
        return e

    feast_parquet_dir = get_ws_feast_parquet_dir(workspace_id)
    file_list = glob.glob(feast_parquet_dir + '/*.parquet')

    df_list = list()
    for parquet_path in sorted(file_list):
        df_list.append(pandas.read_parquet(parquet_path))

    feast_parquet_path = get_pj_parquet_path(workspace_id, project_id)
    pandas.concat(df_list).to_parquet(feast_parquet_path, index=False)

    return feast_parquet_path


def __combine_files(dir_path: str, file_path: str, contents: str):
    file_list = glob.glob(dir_path + '/*.txt')
    with open(file_path, 'w') as fs_file:
        fs_file.write(contents)
        for file_name in sorted(file_list):
            with open(file_name, 'r') as f:
                fs_file.write(f.read())

async def perform_apply(workspace_id: int):
    ws_feast_path = get_ws_feast_path(workspace_id)

    fv_dir = get_ws_feast_fv_dir(workspace_id)
    fv_file_path = get_ws_features(workspace_id)
    __combine_files(dir_path=fv_dir, file_path=fv_file_path, contents=get_features_import_libs(workspace_id))

    source_dir = get_ws_feast_source_dir(workspace_id)
    source_file_path = get_ws_sources(workspace_id)
    __combine_files(dir_path=source_dir, file_path=source_file_path, contents=get_sources_import_libs())

    entity_dir = get_ws_feast_entity_dir(workspace_id)
    entity_file_path = get_ws_entities(workspace_id)
    __combine_files(dir_path=entity_dir, file_path=entity_file_path, contents=get_entities_import_libs())

    os.system(f'feast -c {ws_feast_path} apply')
    return ws_feast_path


async def delete_dataset(workspace_id: int, project_id: int, dataset_id: int):
    pj_parquet_file_path = get_pj_parquet_path(workspace_id, project_id)
    ds_parquet_path = get_base_parquet_path(workspace_id, project_id, dataset_id)

    if os.path.exists(ds_parquet_path):
        df = pandas.read_parquet(pj_parquet_file_path)
        df = df[df[DATASET_COLUMN] != dataset_id]
        df.to_parquet(pj_parquet_file_path, index=False)
        os.system(f'rm {ds_parquet_path}')

    pj_parquet_dir = get_base_parquet_dir(workspace_id, project_id)
    file_list = glob.glob(pj_parquet_dir + '/*.parquet')
    if len(file_list) == 0:
        base_fv = get_base_fv_path(workspace_id, project_id)
        base_source = get_base_source_path(workspace_id, project_id)
        base_entity = get_base_entity_path(workspace_id, project_id)
        os.system(f'rm {" ".join([base_fv, base_source, base_entity])}')
    return ds_parquet_path

async def push_server_boot():
    server_list = glob.glob('/feast_repo/**/*server.pkl', recursive=True)
    for server in server_list:
        with open(server, 'rb') as f:
            res = pickle.load(f)
            subprocess.Popen(res)


def __write_base_fv_file(workspace_id: int, project_id: int, dataset_features: dict):
    base_fv = get_base_fv_path(workspace_id, project_id)
    feature_list = make_features_list(dataset_features)
    contents = get_define_feature_view_contents(project_id, feature_list)
    if not os.path.exists(base_fv):
        __write_file_contents(base_fv, contents)


def __write_base_source_file(workspace_id: int, project_id: int, timestamp_col: str):
    base_source = get_base_source_path(workspace_id, project_id)
    contents = get_define_file_source_contents(workspace_id, project_id, timestamp_col)
    if not os.path.exists(base_source):
        __write_file_contents(base_source, contents)


def __write_base_entity_file(workspace_id: int, project_id: int, entity_name: str, entity_dtype: str):
    base_entity = get_base_entity_path(workspace_id, project_id)
    entity_type = __mapping_feast_type(entity_dtype, ENTITY_DTYPE)
    contents = get_define_entity_contents(project_id, entity_name, entity_type)
    if not os.path.exists(base_entity):
        __write_file_contents(base_entity, contents)


def write_base_file(workspace_id: int, project_id: int, dataset_features: dict, timestamp_col: str, entity_name: str, entity_dtype: str):
    __write_base_fv_file(workspace_id, project_id, dataset_features)
    __write_base_source_file(workspace_id, project_id, timestamp_col)
    __write_base_entity_file(workspace_id, project_id, entity_name, entity_dtype)
