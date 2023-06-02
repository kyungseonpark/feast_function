"""
다른 코드들의 가독성을 높이기 위해,
Feast에서 Hard-Coding으로 구성되어야 하는 부분들을 모아 놓았습니다.
"""

DEFINE_ENTITY_TEMPLATE = '''
{% macro define_entity(val_name, entity_name, entity_type) %}
en_{{ val_name }} = Entity(
    name="{{ entity_name }}",
    value_type={{ entity_type }},
)
{% endmacro %}
{{ define_entity(val_name, entity_name, entity_type) }}\n
'''

DEFINE_FILE_SOURCE_TEMPLATE = '''
{% macro define_file_source(val_name, base_parquet_path, timestamp_col) %}
fs_{{ val_name }} = FileSource(
    path="{{ base_parquet_path }}",
    timestamp_field="{{ timestamp_col }},"
)
{% endmacro %}
{{ define_file_source(val_name, base_parquet_path, timestamp_col) }}\n
'''

DEFINE_PUSH_SOURCE_TEMPLATE = '''
{% macro define_push_source(val_name) %}
# feast push source for streaming data.
ps_{{ val_name }} = PushSource(
    name="ps_{{ val_name }}",
    batch_source=fs_{{ val_name }},
)
{% endmacro %}
{{ define_push_source(val_name) }}\n
'''

DEFINE_FEATURE_VIEW_TEMPLATE = '''
{% macro define_feature_view(val_name, feature_list) %}
fv_{{ val_name }} = FeatureView(
    name="fv_{{ val_name }}",
    source=fs_{{ val_name }},
    entities=[en_{{ val_name }}],
    schema=[{{ feature_list }}],
    ttl=timedelta(seconds=86400 * 30),
)
{% endmacro %}
{{ define_feature_view(val_name, feature_list) }}\n
'''

DEFINE_KAFKA_SOURCE_TEMPLATE = '''
{% macro define_kafka_source(val_name, timestamp_col, schema_json) %}
kas_{{ val_name }} = KafkaSource(
    name="kas_{{ val_name }}",
    kafka_bootstrap_servers="kafka1:19091,kafka2:19092,kafka3:19093",
    topic="topic-{{ val_name.replace("_", "-") }}",
    timestamp_field="{{ timestamp_col }}",
    batch_source=fs_{{ val_name }},
    message_format=JsonFormat(
        schema_json="{{ schema_json|join(", ") }}",
    ),
    watermark_delay_threshold=timedelta(minutes=5),
)
{% endmacro %}
{{ define_kafka_source(val_name, timestamp_col, schema_json) }}\n
'''


# Push-Server를 자식 프로세스(fastAPI)로 실행하기 위해 import 해야하는 라이브러리 모음.
DEFINE_FEAST_PUSH_SERVER = '''
{% macro define_feast_push_server(repo_path) %}
from feast import FeatureStore
from feast.feature_server import get_app
import os
import subprocess
import uvicorn

fs = FeatureStore(repo_path="{{ repo_path }}")
app = get_app(fs)

@app.delete("/shutdown_server")
def shutdown_feast_server():
    os._exit(os.EX_OK)

{% endmacro %}
{{ define_feast_push_server(repo_path) }}\n
'''


# Feature-View 파일을 생성할 때, 필요한 라이브러리를 선언하는 부분.
FEATURES_IMPORT_LIBS = '''
{% macro get_features_import_libs(ws_name) %}
from datetime import timedelta
from pyspark.sql import DataFrame
from feast import (
    FeatureView,
    Field
)
from feast.stream_feature_view import stream_feature_view
from feast.types import Int32, Int64, Float32, Float64, String, Bool, UnixTimestamp

from {{ ws_name }}_entities import *
from {{ ws_name }}_sources import *

{% endmacro %}
{{ get_features_import_libs(ws_name) }}\n
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

