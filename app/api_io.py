from fastapi import Body, UploadFile, Path
from pydantic import BaseModel

WorkspaceID = Body(ge=1, example=1, description="ID of workspace used by ABACUS Studio.")
ProjectID = Body(ge=1, example=1, description="ID of project used by ABACUS Studio.")
DatasetID = Body(ge=1, example=1, description="ID of dataset used by ABACUS Studio.")
RepoPath = Path(description="Feast's repository path")


class FeastInitInput(BaseModel):
    """
    API Body input values for initializing Feast per workspace.

    workspace_id: ID of workspace used by ABACUS Studio.
    """
    workspace_id: int = WorkspaceID


class FeastInitOutput(BaseModel):
    """
    API Body output values after initializing Feast per workspace.

    repo_path: Feast's repository path
    """
    repo_path: str


class FeastDatasetPathInput(BaseModel):
    workspace_id: int = WorkspaceID
    project_id: int = ProjectID
    dataset_id: int = DatasetID


class FeastDatasetPathOutput(BaseModel):
    dataset_path: str


class TransferDatasetInput(BaseModel):
    """
    API Body input values for Input Dataset into Feast.
    ### Inherits from FeastInitInput. Because it depends on Workspace.

    workspace_id: ID of workspace used by ABACUS Studio.
    project_id: ID of project used by ABACUS Studio.
    dataset_id: ID of dataset used by ABACUS Studio.
    dataset: incoming dataset. format is csv or parquet.
    dataset_features:
    timestamp_col:
    entity_name:
    entity_dtype:
    """
    workspace_id: int = WorkspaceID
    project_id: int = ProjectID
    dataset_id: int = DatasetID
    dataset_features: dict[str, str]
    timestamp_col: str
    entity_name: str
    entity_dtype: str


class TransferDatasetOutPut(BaseModel):
    """
    Input a dataset into Feast and see the API body output.

    repo_path: Feast's repository path
    """
    repo_path: str = RepoPath


class DeleteDatasetInput(BaseModel):
    """
    Input required to delete a dataset.
    ### Inherits from FeastInitInput. Because it depends on Workspace.

    dataset_id: ID of dataset used by ABACUS Studio.
    project_id: ID of project used by ABACUS Studio.
    dataset_id: ID of dataset used by ABACUS Studio.
    """
    workspace_id: int = WorkspaceID
    project_id: int = ProjectID
    dataset_id: int = DatasetID


class DeleteDatasetOutPut(BaseModel):
    """
    Output after deleting a dataset.

    removed_file_list:
    """
    removed_file_list: list[str]


class FeastServeInput(BaseModel):
    """
    Input required for the "Feast Serve" action.

    workspace_id: ID of workspace used by ABACUS Studio.
    project_id: ID of project used by ABACUS Studio.
    bootstrap_servers:
    """
    workspace_id: int = WorkspaceID
    project_id: int = ProjectID
    bootstrap_servers: list[str]


class FeastServeOutput(BaseModel):
    """
    Output after Serve Feast push server.

    container_name:
    """
    container_name: str


class StopServingInput(BaseModel):
    """
    Input required to stop serving.

    project_id: ID of project used by ABACUS Studio.
    """
    project_id: int = ProjectID


class StopServingOutput(BaseModel):
    """
    Output after Stop serving.

    container_name:
    """
    container_name: str


class FeastPushDataInput(BaseModel):
    """

    workspace_id: ID of workspace used by ABACUS Studio.
    project_id: ID of project used by ABACUS Studio.
    input_data:
    """
    workspace_id: int = WorkspaceID
    project_id: int = ProjectID
    input_data: dict[str, list]


class FeastPushDataOutput(BaseModel):
    """

    msg:
    """
    msg: str
