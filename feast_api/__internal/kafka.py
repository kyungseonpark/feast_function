import docker
from __constant.feast_global import FEAST_URL
from __constant.feast_template.kafka import *

async def serve_kafka_consumer(workspace_id: int, project_id: int, kafka_bootstrap_servers: list[str]):
    client = docker.from_env()
    container_name = get_consumer_container_name(project_id)
    client.containers.run(
        image='feast_consumer:0.1',
        detach=True,
        environment={
            'FEAST_URL': FEAST_URL,
            'WORKSPACE_ID': workspace_id,
            'PROJECT_ID': project_id,
            'KAFKA_TOPIC': get_response_kafka_topic(project_id),
            'KAFKA_BOOTSTRAP_SERVERS': ','.join(kafka_bootstrap_servers),
        },
        name=container_name,
        remove=True
    )
    return container_name

async def shutdown_kafka_consumer(project_id: int):
    client = docker.from_env()
    container_name = get_consumer_container_name(project_id)
    con = client.containers.get(container_name)
    con.stop()
    return container_name
