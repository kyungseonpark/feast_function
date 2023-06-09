from feast_api.__internal.__constant.feast_template.path.feast_path_template import PJ_NAME

RESPONSE_KAFKA_TOPIC = f'{PJ_NAME.replace("_","-",1)}-response'
CONSUMER_CONTAINER_NAME = f'feast-consumer-{PJ_NAME}'
