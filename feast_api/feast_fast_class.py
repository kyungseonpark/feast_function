from typing import Optional, BinaryIO
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

class FeastInitInput(BaseModel):
    workspace_id: int
    project_id: int

class FeastInitOutput(BaseModel):
    repo_path: str

class TransferDatasetInput(FeastInitInput):
    dataset_id: int
    dataset: BinaryIO

class TransferDatasetOutPut(BaseModel):
    dataset_path: str

class FeastApplyInput(FeastInitInput):
    dataset_id: int
    dataset_features: dict
    entity_name: str

class FeastApplyOutput(FeastInitOutput):
    pass

class DeleteDatasetInput(FeastInitInput):
    dataset_id: int

class DeleteDatasetOutPut(BaseModel):
    removed_file_list: list[str]

class FeastServeInput(FeastInitInput):
    bootstrap_servers: list[str]

class FeastServeOutput(BaseModel):
    container_name: str

class StopServingInput(FeastInitInput):
    pass

class StopServingOutput(FeastServeOutput):
    pass
