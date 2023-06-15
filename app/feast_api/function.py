import asyncio

from fastapi import UploadFile
from ._internal import *


async def feast_init(workspace_id: int) -> str:
    """
    Creates the Directory and base files needed to configure a workspace-specific feature store.

        :param workspace_id: ID of the workspace used by ABACUS

        :return: Directory name for the created Feature Store
    """
    await make_feast_dirs(workspace_id)
    repo_path = await make_feast_init_files(workspace_id)
    return repo_path


def feast_dataset_path(workspace_id: int, project_id: int, dataset_id: int):
    return make_feast_dataset_path(workspace_id, project_id, dataset_id)


async def feast_save_parquet_file(
        workspace_id: int,
        project_id: int,
        dataset_id: int,
        parquet_file: UploadFile,
        dataset_features: dict,
        timestamp_col: str,
        entity_name: str,
        entity_dtype: str
):
    """
    Write the files needed to define the Feature Store, such as Feature View, Source, and Entity.

        :param workspace_id: ID of the workspace used by ABACUS
        :param project_id: ID of the project used by ABACUS
        :param dataset_id: ID of the dataset used by ABACUS
        :param parquet_file:
        :param dataset_features:
        :param timestamp_col:
        :param entity_name:
        :param entity_dtype:
        :return:
    """
    save_parquet_tasks = [
        save_parquet_file(workspace_id, project_id, dataset_id, parquet_file),
        write_base_file(workspace_id, project_id, dataset_features, timestamp_col, entity_name, entity_dtype)
    ]
    await asyncio.gather(*save_parquet_tasks)


async def feast_apply(workspace_id: int):
    """
    Define Feature View and feast apply.

        :param workspace_id: ID of the workspace used by ABACUS

        :return: Directory path for the applied Feature Store
    """
    return perform_apply(workspace_id)


async def feast_delete_project(project_id: int):
    await delete_project(project_id)


async def feast_delete_dataset(workspace_id: int, project_id: int, dataset_id: int):
    await delete_dataset(workspace_id, project_id, dataset_id)


async def feast_push_server_boot():
    """
    After the Feast-server is shut down in any action, push-server is automatically executed.
    장애가 발생하거나 강제종료되어 feast-server가 종료된 후, 다시 재가동 하면 push-server도 자동으로 실행되기 위한 함수.
    """
    await push_server_boot()


async def feast_serve_kafka_consumer(workspace_id: int, project_id: int, kafka_bootstrap_servers: list[str]):
    await serve_kafka_consumer(workspace_id, project_id, kafka_bootstrap_servers)


async def feast_shutdown_kafka_consumer(project_id: int):
    await shutdown_kafka_consumer(project_id)

async def feast_push_data(workspace_id: int, project_id: int, input_data: dict[str, list]):
    await push_data(workspace_id, project_id, input_data)
