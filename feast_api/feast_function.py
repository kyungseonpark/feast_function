import glob
import json
import pickle
import pandas
import oyaml
import docker
import pandas as pd
import subprocess
from functools import wraps
from fastapi import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import Optional, Union, List, Dict

from feast import FeatureStore
from feast.data_source import PushMode
from feast_define import *


def feast_push_server_boot():
    """
    After the Feast-server is shut down in any action, push-server is automatically executed.
    장애가 발생하거나 강제종료되어 feast-server가 종료된 후, 다시 재가동 하면 push-server도 자동으로 실행되기 위한 함수.
    """
    server_list = glob.glob('/feast_repo/**/*server.pkl', recursive=True)
    for server in server_list:
        with open(server, 'rb') as f:
            res = pickle.load(f)
            subprocess.Popen(res)

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

