from functools import wraps
from fastapi import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

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

