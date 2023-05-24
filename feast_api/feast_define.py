import pandas as pd
from typing import Optional
from feast_templete import *
from feast_global import *

def define_feast_yaml(
        project: str,
        registry: str,
        provider: str,
        offline_type: str,
        online_type: str
) -> dict:
    res = dict()
    res['project'] = project
    res['registry'] = registry
    res['provider'] = provider

    res['offline_store'] = dict()
    if offline_type == AWS_TYPE:
        pass
    elif offline_type == GCP_TYPE:
        pass
    elif offline_type == FILE_TYPE:
        res['offline_store']['type'] = FILE_TYPE

    # res['online_store'] = dict()
    # if online_type == AWS_TYPE:
    #     pass
    # elif online_type == GCP_TYPE:
    #     pass
    # elif online_type == REDIS_TYPE:
    #     res['online_store']['type'] = REDIS_TYPE
    #     res['online_store']['connection_string'] = 'feast_online_store:6379'

    return res


def define_entity(
        val_name: str,
        entity_name: str,
        entity_dtype: str):
    return f'en_{val_name} = Entity(\n' \
           f'    name="{entity_name}",\n' \
           f'    value_type={_mapping_feast_type(entity_dtype, is_entity=True)}\n' \
           f')\n\n'


def _mapping_feast_type(input_type, is_entity: Optional[bool] = False):
    type_mapping = ENTITY_DTYPE if is_entity else FEATURE_VIEW_DTYPE
    return FEAST_DTYPE[input_type][type_mapping]


def define_file_source(
        val_name: str,
        base_parquet_path: str,
        timestamp_col: str):
    return f'fs_{val_name} = FileSource(\n' \
           f'    path="{base_parquet_path}",\n' \
           f'    timestamp_field="{timestamp_col}"\n' \
           f')\n\n'


def define_push_source(val_name):
    return f'# feast push source for streaming data\n' \
           f'ps_{val_name} = PushSource(\n' \
           f'   name="ps_{val_name}",\n' \
           f'   batch_source=fs_{val_name},\n' \
           f')\n\n'


def define_feature_view(
        val_name: str,
        dataset_features: dict):
    res = f'fv_{val_name} = FeatureView(\n' \
          f'    name="fv_{val_name}",\n' \
          f'    source=fs_{val_name},\n' \
          f'    entities=[en_{val_name}],\n' \
          f'    schema=[{_make_features_list(dataset_features)}],\n' \
          f'    ttl=timedelta(seconds=(86400 * 30)),\n'
    res += f')\n\n'
    return res


def define_kafka_source(
        val_name: str,
        timestamp_col: str,
        dataset_features: dict,
):
    schema_json = list()
    for k, v in dataset_features.items():
        schema_json.append(f'{k} {FEAST_DTYPE[v][KAFKA_DTYPE]}')
    schema_json.append(f'{timestamp_col} {FEAST_DTYPE["UNIX_TIMESTAMP"][KAFKA_DTYPE]}')
    res = f'kas_{val_name} = KafkaSource(\n' \
          f'    name="kas_{val_name}",\n' \
          f'    kafka_bootstrap_servers="kafka1:19091,kafka2:19092,kafka3:19093",\n' \
          f'    topic="topic-{val_name.replace("_", "-")}",\n' \
          f'    timestamp_field="{timestamp_col}",\n' \
          f'    batch_source=fs_{val_name},\n' \
          f'    message_format=JsonFormat(\n' \
          f'        schema_json="{", ".join(schema_json)}",\n' \
          f'    ),\n' \
          f'    watermark_delay_threshold=timedelta(minutes=5),\n' \
          f')\n\n'

    return res


# def define_stream_feature_view(
#         val_name: str,
#         derived_features: dict,
#         timestamp_col: str,
# ):
#     """
#     :param timestamp_col:
#     :param val_name:
#     :param derived_features:
#     {
#         new_feature_name_1 : {
#             option: "sum",
#             bef_feat: ["V1", "V2", "V3"],
#             new_dtype: "FLOAT",
#         },
#         new_feature_name_2 : {
#             option: "avg",
#             bef_feat: ["V11", "V12"],
#             new_dtype: "FLOAT",
#         }
#     }
#     :return:
#     """
#     sfv_res = f'@stream_feature_view(\n' \
#               f'    entities=[en_{val_name}],\n' \
#               f'    ttl=timedelta(seconds=8640000000),\n' \
#               f'    mode="spark",\n'
#
#     schema = f'    schema=[\n'
#     for k, v in derived_features.items():
#         schema += f'        Field(name="{k}", dtype={FEAST_DTYPE[v["new_dtype"]][FEATURE_VIEW_DTYPE]}),\n'
#     sfv_res += schema
#     sfv_res += f'    ],\n'
#
#     sfv_res += f'    timestamp_field="{timestamp_col}",\n'
#     sfv_res += f'    online=True,\n'
#     sfv_res += f'    source=kas_{val_name},\n' \
#                f')\n'
#
#     stream_func = f'def kas_{val_name}_stream(df: DataFrame):\n' \
#                   f'    from pyspark.sql.functions import col, sum\n\n' \
#                   f'    return (\n'
#
#     derived_val = f'        df'
#     drop_col = []
#     for k, v in derived_features.items():
#         derived_arithmetic = None
#
#         bef_feat = v['bef_feat']
#         tmp_feat = list()
#         for feat in bef_feat:
#             if type(feat) is str:
#                 tmp_feat.append(f'col("{feat}")')
#                 drop_col.append(f'"{feat}"')
#             elif type(feat) is int:
#                 tmp_feat.append(f'{feat}')
#
#         if v['option'] in ('sum', 'avg'):
#             derived_arithmetic = f'({" + ".join(tmp_feat)})'
#             if v['option'] == 'avg':
#                 derived_arithmetic += f'/{len(bef_feat)}'
#         elif v['option'] == 'sub':
#             derived_arithmetic = f'({" - ".join(tmp_feat)})'
#         else:
#             pass
#
#         derived_val += f'.withColumn("{k}", {derived_arithmetic})'
#     if len(drop_col) != 0:
#         derived_val += f'\n        .drop({", ".join(list(set(drop_col)))})'
#     derived_val += f'\n    )\n\n'
#
#     return sfv_res + stream_func + derived_val


def _make_features_list(dataset_features: dict):
    """Make list of Features."""
    res_list = list()
    for key, item in dataset_features.items():
        res_list.append(f'\n        Field(name="{key}", dtype={_mapping_feast_type(item)})')
    return ','.join(res_list)


def define_feast_push_server(repo_path: str):
    res = FEAST_PUSH_SERVER_IMPORT_LIBS
    res += f'fs = FeatureStore(repo_path="{repo_path}")\n'
    res += 'app = get_app(fs)\n\n'
    for _, val in PUSH_SERVER_APIS.items():
        res += val
    return res


def define_feast_push_server_cli(
        pj_name: str,
        host_ip: str,
        server_port,
        repo_path: str):
    return [
            'uvicorn', f'{pj_name}_server:app',
            '--host', f'{host_ip}',
            '--port', f'{server_port}',
            '--app-dir', f'{repo_path}'
        ]


def get_features_import_libs(ws_name: str):
    res = FEATURES_IMPORT_LIBS
    res += f'from {ws_name}_entities import *\n' \
           f'from {ws_name}_sources import *\n\n'
    return res


def get_sources_import_libs():
    res = SOURCES_IMPORT_LIBS
    return res


def get_entities_import_libs():
    res = ENTITIES_IMPORT_LIBS
    return res


def get_feast_dtype():
    return FEAST_DTYPE


def convert_dtpye_dict(dtpye_dict: dict, dtype_option: str):
    converted_dtpye_dict = dict()
    for k, v in dtpye_dict.items():
        converted_dtpye_dict[k] = FEAST_DTYPE[v][dtype_option]
    return converted_dtpye_dict


def spark_preprocess_fn(rows: pd.DataFrame):
    print(f"df columns: {rows.columns}")
    print(f"df size: {rows.size}")
    print(f"df size: {rows.head}")
    return rows
