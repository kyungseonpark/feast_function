from api_io import *
from fastapi import FastAPI

from feast_api import *


feast = FastAPI(
    title="ABACUS Feast",
    version="0.2.0",
    description=f'Feature Store for ABACUS. 🚛\n\n'
                f'API Docs = https://www.notion.so/aizen-global/Feast-API-API-Scenario-cefb7df9f42e4237b052c696549ba54b'
)

TAGS = ["Initialization", "Prepare", "Deployment"]


@feast.on_event("startup")
async def startup_event():
    """
    Runs when the feast-server starts
    서버가 시작될 때 실행.
    """
    await feast_push_server_boot()


@feast.post("/init/", tags=[TAGS[0]])
async def post_feast_init(api_body: FeastInitInput) -> FeastInitOutput:
    """
    **POST**, init the project feast-repo.
    Recommend when the first dataset is saved in the abacus-project.\n\n

    - **workspace_id**: ID of the workspace used by ABACUS
    """
    repo_path = await feast_init(api_body.workspace_id)
    return FeastInitOutput(
        repo_path=repo_path,
    )


@feast.post("/transfer_and_apply/", tags=[TAGS[1]])
async def post_feast_save_and_apply(api_body: TransferDatasetInput):
    """
    **POST**, API that apply feature-view after sending dataset.\n\n
    }
    """
    print(api_body.dataset_features)
    await feast_save_parquet_file(**api_body.dict()),
    repo_path = await feast_apply(**api_body.dict())
    return TransferDatasetOutPut(repo_path=repo_path)


@feast.delete("/delete_dataset/", tags=[TAGS[1]])
async def delete_feast_dataset(api_body: DeleteDatasetInput):
    """
    **DELETE**, API for deleting Dataset from feast-repo(parquet, FeatureView).\n\n
    :param api_body:
    {
        "workspace_id": 1,
        "project_id": 1,
        "dataset_id": 1,
    }
    :return:
    {
        "dataset_path": "/feast_repo/1_workspace/1_project/data/1_dataset.parquet"
        "base_setting_file_path": "/feast_repo/1_workspace/1_project/data/1_dataset_feast.txt"
    }
    """
    await feast_delete_dataset(**api_body.dict())
    await feast_apply(**api_body.dict())
    return DeleteDatasetOutPut()


@feast.post("/serve/kafka/", tags=[TAGS[2]])
async def post_feast_serve_by_kafka(api_body: FeastServeInput):
    """
    **POST**, API that drives the push-server of the project.\n\n
    :param api_body:
    {
        "workspace_id": 1,
        "project_id": 1,
        "bootstrap_servers": List[str],
    }
    :return:
    {
        "server_address": "host_ip:server_port"
    }
    """
    await feast_serve_kafka_consumer(**api_body.dict())
    return FeastServeOutput()


@feast.post("/shutdown/kafka/", tags=[TAGS[2]])
async def post_shutdown_feast_server(api_body: StopServingInput):
    """
    **POST**, API that shutdown push-server of project.\n\n
    :param api_body:
    {
        "workspace_id": 1,
        "project_id": 1
    }
    :return:
    {
        "server_address": "host_ip:server_port"
    }
    """
    await feast_shutdown_kafka_consumer(**api_body.dict())
    return StopServingOutput()


@feast.post("/push/", tags=[TAGS[2]])
async def post_feast_push_data(api_body: FeastPushDataInput):
    await feast_push_data(**api_body.dict())
    return FeastPushDataOutput()


# @feast.post("/get_historical_features/", response_class=FileResponse)
# async def post_get_historical_features(api_body: FeastServeItem):
#     ws_id = api_body.workspace_id
#     pj_id = api_body.project_id
#     timestamp_col = api_body.timestamp_column
#     res_list = list()
#     frs = None
#     for d in api_body.data:
#         ds_id = d['dataset_id']
#         fdi = FeastServeItem(
#             workspace_id=ws_id,
#             project_id=pj_id,
#             timestamp_column=timestamp_col,
#             dataset_id=ds_id,
#             data=d)
#         frs = FeastRepoServe(fdi)
#         # if ds_id == 0:
#         #     frs.feast_get_online_features()
#         res_list.append(frs.feast_get_training_data())
#
#     file_path = f'{frs.get_data_path()}/ghf_res.parquet'
#     res = pd.concat(res_list)
#     tobe_dtypes = dict()
#     for col, dtype in res.dtypes.to_dict():
#         if dtype == 'object':
#             tobe_dtypes[col] = 'str'
#     res.astype(tobe_dtypes).to_parquet(file_path)
#
#     return file_path
