import os
import glob
import asyncio

from _constant.feast_global import *
from _constant.feast_template.path import get_ws_feast_path, get_pj_name
from _constant.feast_template.path import get_ws_feast_parquet_dir, get_ws_feast_fv_dir
from _constant.feast_template.path import get_ws_feast_source_dir, get_ws_feast_entity_dir


async def __mkdir(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


async def make_feast_dirs(workspace_id: int):
    mkdir_tasks = [
        __mkdir(get_ws_feast_path(workspace_id)),
        __mkdir(get_ws_feast_parquet_dir(workspace_id)),
        __mkdir(get_ws_feast_fv_dir(workspace_id)),
        __mkdir(get_ws_feast_source_dir(workspace_id)),
        __mkdir(get_ws_feast_entity_dir(workspace_id))
    ]
    await asyncio.gather(*mkdir_tasks)


async def delete_project(project_id: int):
    pj_name = get_pj_name(project_id)
    del_files = glob.glob(fr'{FEAST_REPO}/**/*{pj_name}*', recursive=True)
    for file in del_files:
        os.remove(file)


