from .feast_path_template import *
from feast_api.__internal.__constant.feast_template import render_j2_template


def get_ws_name(workspace_id: int):
    return render_j2_template(template_name=WS_NAME, workspace_id=workspace_id)


def get_pj_name(project_id: int):
    return render_j2_template(template_name=PJ_NAME, project_id=project_id)


def get_ds_name(dataset_id: int):
    return render_j2_template(template_name=DS_NAME, dataset_id=dataset_id)


def get_ws_feast_path(workspace_id: int):
    return render_j2_template(template_name=WS_FEAST_PATH, workspace_id=workspace_id)


def get_ws_feast_init_file(workspace_id: int):
    return render_j2_template(template_name=WS_FEAST_INIT_FILE, workspace_id=workspace_id)


def get_ws_feast_config_file(workspace_id: int):
    return render_j2_template(template_name=WS_FEAST_CONFIG_FILE, workspace_id=workspace_id)


def get_ws_feast_parquet_dir(workspace_id: int):
    return render_j2_template(template_name=WS_FEAST_PARQUET_DIR, workspace_id=workspace_id)


def get_ws_feast_fv_dir(workspace_id: int):
    return render_j2_template(template_name=WS_FEAST_FV_DIR, workspace_id=workspace_id)

def get_ws_feast_source_dir(workspace_id: int):
    return render_j2_template(template_name=WS_FEAST_SOURCE_DIR, workspace_id=workspace_id)

def get_ws_feast_entity_dir(workspace_id: int):
    return render_j2_template(template_name=WS_FEAST_ENTITY_DIR, workspace_id=workspace_id)


def get_pj_parquet_path(workspace_id: int, project_id: int):
    return render_j2_template(template_name=PJ_PARQUET_PATH, workspace_id=workspace_id, project_id=project_id)


def get_ws_features(workspace_id: int):
    return render_j2_template(template_name=WS_FEATURES, workspace_id=workspace_id)


def get_ws_sources(workspace_id: int):
    return render_j2_template(template_name=WS_SOURCES, workspace_id=workspace_id)


def get_ws_entities(workspace_id: int):
    return render_j2_template(template_name=WS_ENTITIES, workspace_id=workspace_id)


def get_base_parquet_dir(workspace_id: int, project_id: int):
    return render_j2_template(template_name=BASE_PARQUET_DIR, workspace_id=workspace_id, project_id=project_id)


def get_base_parquet_path(workspace_id: int, project_id: int, dataset_id: int):
    return render_j2_template(
        template_name=BASE_PARQUET_PATH,
        workspace_id=workspace_id,
        project_id=project_id,
        dataset_id=dataset_id
    )


def get_base_fv_path(workspace_id: int, project_id: int):
    return render_j2_template(template_name=BASE_FV_PATH, workspace_id=workspace_id, project_id=project_id)


def get_base_source_path(workspace_id: int, project_id: int):
    return render_j2_template(template_name=BASE_SOURCE_PATH, workspace_id=workspace_id, project_id=project_id)


def get_base_entity_path(workspace_id: int, project_id: int):
    return render_j2_template(template_name=BASE_ENTITY_PATH, workspace_id=workspace_id, project_id=project_id)
