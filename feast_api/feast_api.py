import glob
import pickle
import subprocess

import pandas
from functools import wraps

from fastapi import status
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from feast_function import FeastRepo, FeastDataset, FeastServe
from feast_function import FeastRepoItem, FeastDatasetItem, FeastServeItem
from feast_function import feast_push_server_boot
from feast_global import *

feast = FastAPI(
    title="Feast",
    description=f'Feature Store for ABACUS. 🚛\n\n'
                f'API Docs = https://www.notion.so/aizen-global/Feast-API-API-Scenario-cefb7df9f42e4237b052c696549ba54b'
)

TAGS = ["Repository", "Dataset", "Server"]


@feast.on_event("startup")
async def startup_event():
    """
    Runs when the feast-server starts
    서버가 시작될 때 실행.
    """
    feast_push_server_boot()





@feast.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(exc.errors())
    )


def exception_handler(func):
    """
    Decorator created for debugging when the feast-server encounters an [Internal Server Error].
    feast-server에서 error가 발생했을때 내부에러라고만 출력되어서 Debugging용 데코레이터.
    """
    @wraps(func)
    def execute_func(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except HTTPException as e:
            return JSONResponse(
                status_code=500,
                content=jsonable_encoder({
                    "loc": f'{func.__name__}',
                    "exception": "HTTPException",
                    "msg": f'{e.detail}'
                })
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content=jsonable_encoder({
                    "loc": f'{func.__name__}',
                    "exception": "Exception",
                    "msg": f'{e}'
                })
            )
    return execute_func


def check_api_body(api_body: dict, need_body: list):
    """
    Server핸들링 Request Body 클래스가 Optional로 지저분해져서 Body를 체크해서 필수항목을 확인하기위한 함수.
    :param api_body: 실제로 입력으로 들어온 Body parameter
    :param need_body: 필수로 들어와야하는 Body parameter
    """
    res_list = list()
    for item in need_body:
        if api_body[item] is None:
            res_list.append(item)
    if len(res_list) != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Not Found Item, {res_list}')


@exception_handler
@feast.post("/init/", tags=[TAGS[0]])
async def post_feast_init(api_body: FeastRepoItem):
    """
    **POST**, init the project feast-repo.
    Recommend when the first dataset is saved in the abacus-project.\n\n
    :param api_body:
    {
        "workspace_id": 1,
        "project_id": 1,
    }
    :return:
    {
        "repo_path": "/feast_repo/1_workspace/1_project"
    }
    """
    fr = FeastRepo(api_body)
    return {"repo_path": fr.feast_init()}


@exception_handler
@feast.post("/transfer_dataset/", tags=[TAGS[1]])
async def post_transfer_dataset(
        workspace_id: int = Form(...),
        project_id: int = Form(...),
        dataset_id: int = Form(...),
        dataset: UploadFile = File(...)):
    """
    **POST**, API for transferring the dataset directly to the feast-repo,
    preparing for use in the cloud repository.\n\n
    """
    dataset_file = await dataset.read()
    fdi = FeastDatasetItem(workspace_id=workspace_id, project_id=project_id, dataset_id=dataset_id)
    fdm = FeastDataset(fdi)

    # 전송된 데이터셋 기본 저장.
    dataset_path = fdm.get_base_parquet_path()
    with open(dataset_path, 'wb') as f:
        f.write(dataset_file)
    df = pandas.read_parquet(dataset_path)
    df[DATASET_COLUMN] = dataset_id
    df.to_parquet(dataset_path, index=False)
    await dataset.close()
    fdm.save_parquet_file()
    return {"msg": f'Complete to save dataset.:{dataset_path}'}


@exception_handler
@feast.post("/apply/", tags=[TAGS[1]])
async def post_feast_save_and_apply(api_body: FeastDatasetItem):
    """
    **POST**, API that apply feature-view after sending dataset.\n\n
    :param api_body:
    {
        "workspace_id": 1,
        "project_id": 1,
        "dataset_id": 1,
        "dataset_features": dict(),
        "entity_name": "entity_name",
        "entity_dtype": "FEAST_DTYPE"
        "timestamp_column": "timestamp_column_name"
    }
    :return:
    {
        "base_setting_file_path": "/feast_repo/1_workspace/1_project/data/1_dataset_feast.txt"
        "repo_path": "/feast_repo/1_workspace/1_project"
    }
    """
    fdm = FeastDataset(api_body)
    fdm.write_base_file()
    repo_path = fdm.feast_apply()
    return {
        "repo_path": repo_path
    }


@exception_handler
@feast.delete("/dataset_delete/", tags=[TAGS[1]])
async def del_feast_dataset(api_body: FeastDatasetItem):
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
    fd = FeastDataset(api_body)
    del_res = fd.del_feast_dataset()
    return {
        "remove_file_list": del_res
    }


@exception_handler
@feast.post("/serve/", tags=[TAGS[2]])
def post_feast_serve(api_body: FeastServeItem):
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
    check_api_body(
        api_body=api_body.dict(),
        need_body=[
            'workspace_id',
            'project_id',
        ])
    fsv = FeastServe(api_body)
    return {"container_name": fsv.serve()}


@exception_handler
@feast.post("/push/", tags=[TAGS[2]])
def post_feast_serve(api_body: FeastServeItem):
    """
    **POST**, API that drives the push-server of the project.\n\n
    :param api_body:
    {
        "workspace_id": 1,
        "project_id": 1,
        "input_data": List[Dict],
    }
    :return:
    {
        "server_address": "host_ip:server_port"
    }
    """
    check_api_body(
        api_body=api_body.dict(),
        need_body=[
            'workspace_id',
            'project_id',
            'input_data'
        ])
    fsv = FeastServe(api_body)
    return {"container_name": fsv.push()}


@exception_handler
@feast.post("/shutdown_consumer/", tags=[TAGS[2]])
async def post_shutdown_feast_server(api_body: FeastServeItem):
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
    check_api_body(
        api_body=api_body.dict(),
        need_body=[
            'workspace_id',
            'project_id',
        ])
    fsv = FeastServe(api_body)
    return {"container_name": fsv.shutdown()}


# @exception_handler
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
