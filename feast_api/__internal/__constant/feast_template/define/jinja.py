from .feast_define_templete import *
from feast_api.__internal.__constant.feast_template import render_j2_template

def get_define_entity_contents(project_id: str, entity_name: str, entity_type: str):
    return render_j2_template(template_name=DEFINE_ENTITY_TEMPLATE, project_id=project_id, entity_name=entity_name,
                              entity_type=entity_type)


def get_define_file_source_contents(workspace_id: int, project_id: int, timestamp_col: str):
    return render_j2_template(template_name=DEFINE_FILE_SOURCE_TEMPLATE, workspace_id=workspace_id,
                              project_id=project_id, timestamp_col=timestamp_col)


def get_define_push_source_contents(project_id: str):
    return render_j2_template(template_name=DEFINE_PUSH_SOURCE_TEMPLATE, project_id=project_id)


def get_define_feature_view_contents(project_id: int, feature_list: str):
    return render_j2_template(template_name=DEFINE_FEATURE_VIEW_TEMPLATE, project_id=project_id,
                              feature_list=feature_list)

def get_define_kafka_source_contents(project_id: int, timestamp_col: str, schema_json: str):
    return render_j2_template(template_name=DEFINE_KAFKA_SOURCE_TEMPLATE, project_id=project_id,
                              timestamp_col=timestamp_col, schema_json=schema_json)

def get_define_feast_push_server_contents(repo_path: str):
    return render_j2_template(template_name=DEFINE_FEAST_PUSH_SERVER, repo_path=repo_path)


def get_features_import_libs(workspace_id: int):
    return render_j2_template(template_name=FEATURES_IMPORT_LIBS, workspace_id=workspace_id)


def get_sources_import_libs():
    return render_j2_template(template_name=SOURCES_IMPORT_LIBS)


def get_entities_import_libs():
    return render_j2_template(template_name=ENTITIES_IMPORT_LIBS)
