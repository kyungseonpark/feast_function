"""
Feast에서 Hard-Coding으로 선언되어야할 문자열(String)들을
전연변수로 선언하여 오타로 인한 오동작을 방지하기 위해 만든 파일.
"""

import os

# Feast Repo 절대 주소.
FEAST_REPO = os.getenv('FEAST_HOME', '/feast_repo')
FEAST_URL = os.getenv('FEAST_URL')

# Feast에서는 사용되는 곳마다 Dtype형식이 다르게 선언되기 때문에 FEAST_DTYPE 딕셔너리를 통해 매핑.
FEATURE_VIEW_DTYPE = 'FeatureView'
ENTITY_DTYPE = 'Entity'
KAFKA_DTYPE = 'Kafka'
DATAFRAME_DTYPE = 'DataFrame'

# 아래 주소를 참고하여 데이터 형식을 규약.
# https://github.com/feast-dev/feast/blob/master/docs/specs/offline_store_format.md
FEAST_DTYPE = {
    'UNIX_TIMESTAMP': {
        FEATURE_VIEW_DTYPE: 'UnixTimestamp',
        ENTITY_DTYPE: 'ValueType.UNIX_TIMESTAMP',
        KAFKA_DTYPE: 'timestamp',
        DATAFRAME_DTYPE: 'datetime64[ns]'
    },
    'INT32': {
        FEATURE_VIEW_DTYPE: 'Int32',
        ENTITY_DTYPE: 'ValueType.INT32',
        KAFKA_DTYPE: 'integer',
        DATAFRAME_DTYPE: 'int32'
    },
    'INT64': {
        FEATURE_VIEW_DTYPE: 'Int64',
        ENTITY_DTYPE: 'ValueType.INT32',
        KAFKA_DTYPE: 'long',
        DATAFRAME_DTYPE: 'int64'
    },
    'FLOAT': {
        FEATURE_VIEW_DTYPE: 'Float32',
        ENTITY_DTYPE: 'ValueType.FLOAT32',
        KAFKA_DTYPE: 'float',
        DATAFRAME_DTYPE: 'float32'
    },
    'DOUBLE': {
        FEATURE_VIEW_DTYPE: 'Float64',
        ENTITY_DTYPE: 'ValueType.Float64',
        KAFKA_DTYPE: 'double',
        DATAFRAME_DTYPE: 'float64'
    },
    'STRING': {
        FEATURE_VIEW_DTYPE: 'String',
        ENTITY_DTYPE: 'ValueType.STRING',
        KAFKA_DTYPE: 'string',
        DATAFRAME_DTYPE: 'object'
    },
    'BOOL': {
        FEATURE_VIEW_DTYPE: 'Bool',
        ENTITY_DTYPE: 'ValueType.BOOL',
        KAFKA_DTYPE: 'boolean',
        DATAFRAME_DTYPE: 'bool'
    }
}

# TODO: aws, gcp는 추후에 추가 하고 싶어서 넣어놓음.
# Feast에서 사용할 수 있는 Data-Source Type을 정리.
AWS_TYPE = 'aws'
GCP_TYPE = 'gcp'
FILE_TYPE = 'file'
REDIS_TYPE = 'redis'

# Feast Contents
WS_FEAST = 'feast'
PARQUET_FILE = 'parquet'
ENTITY = 'entity'
FILE_SOURCE = 'source'
FEATURE_VIEW = 'feature_view'

STREAM_PARQUET = 'stream_parquet'
KAFKA_SOURCE = 'kafka_source'
STREAM_FV = 'stream_feature_view'

# dataset의 입출력을 위해 Dataset ID로 구분하는 column이 필요함.
DATASET_COLUMN = 'dataset_id'
