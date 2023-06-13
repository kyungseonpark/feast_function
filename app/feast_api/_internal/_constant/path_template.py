"""
TBD
"""

from .global_variable import FEAST_REPO

WS_NAME = 'workspace_{{ workspace_id }}'
PJ_NAME = 'project_{{ project_id }}'
DS_NAME = 'dataset_{{ dataset_id }}'

WS_FEAST_PATH = f'{FEAST_REPO}/{WS_NAME}'
WS_FEAST_INIT_FILE = f'{WS_FEAST_PATH}/__init__.py'
WS_FEAST_CONFIG_FILE = f'{WS_FEAST_PATH}/feature_store.yaml'

WS_FEAST_PARQUET_DIR = f'{WS_FEAST_PATH}/parquet'
WS_FEAST_FV_DIR = f'{WS_FEAST_PATH}/fv'
WS_FEAST_SOURCE_DIR = f'{WS_FEAST_PATH}/sources'
WS_FEAST_ENTITY_DIR = f'{WS_FEAST_PATH}/entities'

PJ_PARQUET_PATH = f'{WS_FEAST_PARQUET_DIR}/{PJ_NAME}_file_store.parquet'
WS_FEATURES = f'{WS_FEAST_PATH}/{WS_NAME}_features.py'
WS_SOURCES = f'{WS_FEAST_PATH}/{WS_NAME}_sources.py'
WS_ENTITIES = f'{WS_FEAST_PATH}/{WS_NAME}_entities.py'

BASE_PARQUET_DIR = f'{WS_FEAST_PARQUET_DIR}/{PJ_NAME}'
BASE_PARQUET_PATH = f'{BASE_PARQUET_DIR}/{DS_NAME}.parquet'
BASE_FV_PATH = f'{WS_FEAST_FV_DIR}/{PJ_NAME}_base_fv.txt'
BASE_SOURCE_PATH = f'{WS_FEAST_SOURCE_DIR}/{PJ_NAME}_base_source.txt'
BASE_ENTITY_PATH = f'{WS_FEAST_ENTITY_DIR}/{PJ_NAME}_entity.txt'
