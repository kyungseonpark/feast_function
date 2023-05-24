"""
다른 코드들의 가독성을 높이기 위해,
Feast에서 Hard-Coding으로 구성되어야 하는 부분들을 모아 놓았습니다.
"""


# Feature-View파일을 생성할 때, 필요한 라이브러리를 선언하는 부분.
FEATURES_IMPORT_LIBS = f'from datetime import timedelta\n' \
                       f'from pyspark.sql import DataFrame\n' \
                       f'from feast import (\n' \
                       f'    FeatureView,\n' \
                       f'    Field\n' \
                       f')\n' \
                       f'from feast.stream_feature_view import stream_feature_view\n' \
                       f'from feast.types import Int32, Int64, Float32, Float64, String, Bool, UnixTimestamp\n\n' \


SOURCES_IMPORT_LIBS = f'from datetime import timedelta\n' \
                      f'from feast import (\n' \
                      f'    FileSource,\n' \
                      f'    KafkaSource\n' \
                      f')\n' \
                      f'from feast.data_format import JsonFormat\n\n'


ENTITIES_IMPORT_LIBS = f'from feast import (\n' \
                       f'    Entity,\n' \
                       f'    ValueType,\n' \
                       f')\n\n'


# Push-Server를 자식프로세스(fastAPI)로 실행하기 위해 import 해야하는 라이브러리 모음.
FEAST_PUSH_SERVER_IMPORT_LIBS = f'from feast import FeatureStore\n' \
                                f'from feast.feature_server import get_app\n' \
                                f'import os\n' \
                                f'import subprocess\n' \
                                f'import uvicorn\n\n'


# Push-Server를 구동 정지 하기위한 API (Shutdown Server)
PUSH_SERVER_APIS = {
    "shutdown_server":
        f'@app.delete("/shutdown_server")\n'
        f'def shutdown_fesat_server():\n'
        f'    os._exit(os.EX_OK)\n\n'
}
