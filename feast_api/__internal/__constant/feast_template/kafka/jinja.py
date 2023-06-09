from .feast_kafka_template import *
from feast_api.__internal.__constant.feast_template import render_j2_template


def get_response_kafka_topic(project_id: int):
    return render_j2_template(template_name=RESPONSE_KAFKA_TOPIC, project_id=project_id)


def get_consumer_container_name(project_id: int):
    return render_j2_template(template_name=CONSUMER_CONTAINER_NAME, project_id=project_id)
