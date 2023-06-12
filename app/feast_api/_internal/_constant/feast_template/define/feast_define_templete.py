"""
다른 코드들의 가독성을 높이기 위해,
Feast에서 Hard-Coding으로 구성되어야 하는 부분들을 모아 놓았습니다.
"""

from feast_api._internal._constant.feast_template.path.feast_path_template import (
    WS_NAME,
    PJ_NAME,
    WS_FEAST_PATH,
    PJ_PARQUET_PATH
)

ENTITY_DEFINE_NAME = f'en_{PJ_NAME}'
FEATURE_VIEW_DEFINE_NAME = f'fv_{PJ_NAME}'

FILE_SOURCE_DEFINE_NAME = f'fs_{PJ_NAME}'
PUSH_SOURCE_DEFINE_NAME = f'ps_{PJ_NAME}'
KAFKA_SOURCE_DEFINE_NAME = f'kas_{PJ_NAME}'


DEFINE_ENTITY_TEMPLATE = f'''
{ENTITY_DEFINE_NAME} = Entity(
    name="{{{{ entity_name }}}}",
    value_type={{{{ entity_type }}}},
)

'''


# need. workspace_id, project_id, timestamp_col
DEFINE_FILE_SOURCE_TEMPLATE = f'''
{FILE_SOURCE_DEFINE_NAME} = FileSource(
    path="{PJ_PARQUET_PATH}",
    timestamp_field="{{{{ timestamp_col }}}},"
)

'''


DEFINE_PUSH_SOURCE_TEMPLATE = f'''
# feast push source for streaming data.
{PUSH_SOURCE_DEFINE_NAME} = PushSource(
    name="{PUSH_SOURCE_DEFINE_NAME}",
    batch_source={FILE_SOURCE_DEFINE_NAME},
)

'''


DEFINE_FEATURE_VIEW_TEMPLATE = f'''
{FEATURE_VIEW_DEFINE_NAME} = FeatureView(
    name="{FEATURE_VIEW_DEFINE_NAME}",
    source={FILE_SOURCE_DEFINE_NAME},
    entities=[{ENTITY_DEFINE_NAME}],
    schema=[{{{{ feature_list }}}}],
    ttl=timedelta(seconds=86400 * 30),
)

'''


DEFINE_KAFKA_SOURCE_TEMPLATE = f'''
{KAFKA_SOURCE_DEFINE_NAME} = KafkaSource(
    name="{KAFKA_SOURCE_DEFINE_NAME}",
    kafka_bootstrap_servers="kafka1:19091,kafka2:19092,kafka3:19093",
    topic="topic-{PJ_NAME.replace("_", "-", 1)}",
    timestamp_field="{{{{ timestamp_col }}}}",
    batch_source={FILE_SOURCE_DEFINE_NAME},
    message_format=JsonFormat(
        schema_json="{{{{ schema_json }}}}",
    ),
    watermark_delay_threshold=timedelta(minutes=5),
)

'''


# Push-Server를 자식 프로세스(fastAPI)로 실행하기 위해 import 해야하는 라이브러리 모음.
DEFINE_FEAST_PUSH_SERVER = f'''
from feast import FeatureStore
from feast.feature_server import get_app
import os
import subprocess
import uvicorn

fs = FeatureStore(repo_path="{WS_FEAST_PATH}")
app = get_app(fs)

@app.delete("/shutdown_server")
def shutdown_feast_server():
    os._exit(os.EX_OK)

'''


# Feature-View 파일을 생성할 때, 필요한 라이브러리를 선언하는 부분.
FEATURES_IMPORT_LIBS = f'''
from datetime import timedelta
from pyspark.sql import DataFrame
from feast import (
    FeatureView,
    Field
)
from feast.stream_feature_view import stream_feature_view
from feast.types import Int32, Int64, Float32, Float64, String, Bool, UnixTimestamp

from {WS_NAME}_entities import *
from {WS_NAME}_sources import *

'''


SOURCES_IMPORT_LIBS = '''
from datetime import timedelta
from feast import (
    FileSource,
    KafkaSource
)
from feast.data_format import JsonFormat
'''


ENTITIES_IMPORT_LIBS = '''
from feast import (
    Entity,
    ValueType,
)
'''
