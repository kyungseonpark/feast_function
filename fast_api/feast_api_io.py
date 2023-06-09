from typing import BinaryIO
from fastapi import Body, UploadFile
from pydantic import BaseModel


class FeastInitInput(BaseModel):
    """
    API Body input values for initializing Feast per workspace.

    workspace_id: ID of workspace used by ABACUS Studio.
    """
    workspace_id: int = Body(ge=1, example=1)


class FeastInitOutput(BaseModel):
    """
    API Body output values after initializing Feast per workspace.

    repo_path: Feast's repository path
    """
    repo_path: str


class TransferDatasetInput(FeastInitInput):
    """
    API Body input values for Input Dataset into Feast.
    ### Inherits from FeastInitInput. Because it depends on Workspace.

    dataset_id: ID of dataset used by ABACUS Studio.
    dataset: incoming dataset. format is csv or parquet.
    """
    workspace_id: int = Body(ge=1, example=1)
    project_id: int = Body(ge=1, example=1)
    dataset_id: int = Body(ge=1, example=1)
    dataset: UploadFile
    dataset_features: dict
    timestamp_col: str
    entity_name: str
    entity_dtype: str


class TransferDatasetOutPut(BaseModel):
    """
    Input a dataset into Feast and see the API body output.

    repo_path: Feast's repository path
    """
    repo_path: str


class FeastApplyInput(FeastInitInput):
    """
    API inputs required Feast Apply.
    ### Inherits from FeastInitInput. Because it depends on Workspace.
    """
    dataset_id: int
    dataset_features: dict
    entity_name: str

class FeastApplyOutput(FeastInitOutput):
    """
    Feast Apply, and the output value.
    ### Inherits from FeastInitOutput.
    """
    pass

class DeleteDatasetInput(FeastInitInput):
    """
    Input required to delete a dataset.
    ### Inherits from FeastInitInput. Because it depends on Workspace.
    """
    workspace_id: int = Body(ge=1, example=1)
    project_id: int = Body(ge=1, example=1)
    dataset_id: int = Body(ge=1, example=1)

class DeleteDatasetOutPut(BaseModel):
    """
    Output after deleting a dataset.
    """
    removed_file_list: list[str]

class FeastServeInput(FeastInitInput):
    """
    Input required for the "Feast Serve" action.
    """
    workspace_id: int = Body(ge=1, example=1)
    project_id: int = Body(ge=1, example=1)
    bootstrap_servers: list[str]

class FeastServeOutput(BaseModel):
    """
    Output after Serve Feast push server.
    """
    container_name: str

class StopServingInput(FeastInitInput):
    """
    Input required to stop serving.
    """
    pass

class StopServingOutput(FeastServeOutput):
    """
    Output after Stop serving.
    """
    pass
