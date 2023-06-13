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