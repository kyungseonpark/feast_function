import os

import oyaml
import glob

from feast_global import *
from feast_define import *

class FeastPath:
    def __init__(self, workspace_id: int):
        self.ws_name = f'workspace_{workspace_id}'
        self.ws_feast_path = f'{FEAST_REPO}/{self.ws_name}'
        os.makedirs(self.ws_feast_path, exist_ok=True)


class FeastDirectoryPath(FeastPath):
    def __init__(self, workspace_id: int):
        super().__init__(workspace_id)
        self.parquet_path = f'{self.ws_feast_path}/parquet'
        os.makedirs(self.parquet_path, exist_ok=True)

        self.feature_view_path = f'{self.ws_feast_path}/fv'
        os.makedirs(self.feature_view_path, exist_ok=True)

        self.source_path = f'{self.ws_feast_path}/sources'
        os.makedirs(self.source_path, exist_ok=True)

        self.entity_path = f'{self.ws_feast_path}/entities'
        os.makedirs(self.ws_feast_path, exist_ok=True)

        self.repo_fv_file = f'{self.feature_view_path}/{self.ws_name}_features.py'
        self.repo_sources_file = f'{self.source_path}/{self.ws_name}_sources.py'
        self.repo_entities_file = f'{self.entity_path}/{self.ws_name}_entities.py'


class FeastFilePath(FeastDirectoryPath):
    def __init__(self, workspace_id: int, project_id: int, dataset_id: int):
        super().__init__(workspace_id)
        self.pj_name = f'project_{project_id}'
        self.repo_parquet_file = f'{self.parquet_path}/{self.pj_name}_file_store.parquet'
        self.repo_fv_file = f'{self.feature_view_path}/{self.ws_name}_features.py'
        self.repo_sources_file = f'{self.source_path}/{self.ws_name}_sources.py'
        self.repo_entities_file = f'{self.entity_path}/{self.ws_name}_entities.py'


class FeastRepo(FeastDirectoryPath):
    """Class for controlling the Feast Repository."""
    def __init__(self, workspace_id):
        # workspace 당 1개씩 생성.
        super().__init__(workspace_id)

    def feast_init(self):
        with open(self.ws_feast_path + "/__init__.py", "w", encoding="utf-8"):
            pass
        with open(self.ws_feast_path + "/feature_store.yaml", "w", encoding="utf-8") as f:
            oyaml.dump(self.__feast_yaml(), f)
        return self.ws_feast_path

    def feast_apply(self):
        """Define Feature View and feast apply."""
        for key, path in self._repo_path.items():
            # 각 속성들 저장해놓은 txt 파일 경로 호출.
            file_list = glob.glob(path+'/*.txt')
            # 속성별 Feature Store의 경로와 속성별 호출해야할 라이브러리 가져오기
            if key == FEATURE_VIEW:
                file_path = self._repo_fv_file
                import_libs = get_features_import_libs(self._ws_name)
            elif key == FILE_SOURCE:
                file_path = self._repo_sources_file
                import_libs = get_sources_import_libs()
            elif key == ENTITY:
                file_path = self._repo_entities_file
                import_libs = get_entities_import_libs()
            else:
                continue

            # 속성 내용들 저장.
            with open(file_path, 'w') as fs_file:
                fs_file.write(import_libs)
                for file_name in sorted(file_list):
                    with open(file_name, 'r') as f:
                        fs_file.write(f.read())
        # Feast apply
        os.system(f'feast -c {self._ws_feast_path} apply')
        return self._ws_feast_path

    def feast_pj_delete(self):
        del_files = glob.glob(fr'{FEAST_REPO}/**/*{self._pj_name}*', recursive=True)
        for file in del_files:
            os.remove(file)

    def __feast_yaml(self):
        """Make feast setting dict for feast yaml."""
        return define_feast_yaml(
            project=self.ws_name,
            registry=f'{self.ws_name}.db',
            provider='local',
            offline_type=FILE_TYPE,
            online_type=REDIS_TYPE
        )


class FeastDataset(FeastRepo):
    """Class for modifying Feast Dataset."""
    def __init__(self, workspace_id, project_id, dataset_id, dataset):
        super().__init__(workspace_id)
        self._dataset_id = dataset_id
        self._pj_name = f'project_{project_id}'
        self._ds_name = f'dataset_{dataset_id}'

        # self._dataset_features = item.dataset_features
        # self._entity_name = item.entity_name
        # self._entity_dtype = item.entity_dtype
        # self._timestamp_col = item.timestamp_column

        self._repo_parquet_file = f'{self.parquet_path}/{self._pj_name}_file_store.parquet'
        self._repo_fv_file = f'{self.feature_view_path}/{self._ws_name}_features.py'
        self._repo_sources_file = f'{self.source_path}/{self._ws_name}_sources.py'
        self._repo_entities_file = f'{self.entity_path}/{self._ws_name}_entities.py'

        self._base_file_path = {
            PARQUET_FILE: f'{self._repo_path[PARQUET_FILE]}/{self._pj_name}/{self._ds_name}.parquet',
            ENTITY: f'{self._repo_path[ENTITY]}/{self._pj_name}_entity.txt',
            FILE_SOURCE: f'{self._repo_path[FILE_SOURCE]}/{self._pj_name}_base_source.txt',
            FEATURE_VIEW: f'{self._repo_path[FEATURE_VIEW]}/{self._pj_name}_base_fv.txt',
        }

    def get_base_parquet_path(self):
        res = self._base_file_path[PARQUET_FILE]
        pj_parquet_path = os.path.dirname(res)
        os.makedirs(pj_parquet_path, exist_ok=True)
        return res

    def save_parquet_file(self):
        # parquet파일을 합침.
        # TBD: pyarrow로 속도향상 필요함.
        path = f'{self._repo_path[PARQUET_FILE]}/{self._pj_name}'
        file_list = glob.glob(path + '/*.parquet')
        df_list = list()
        for parquet_path in sorted(file_list):
            df_list.append(pandas.read_parquet(parquet_path))
        file_path = self._repo_parquet_file
        pandas.concat(df_list).to_parquet(file_path, index=False)

        return self._ws_feast_path

    def del_feast_dataset(self):
        rm_file_list = list()

        # TBD: pyarrow로 속도 올려야함. 플로우 맞는지 확인하려고 우선 둠.
        parquet_file_path = self._repo_parquet_file
        if os.path.exists(parquet_file_path):
            df = pandas.read_parquet(parquet_file_path)
            df = df[df[DATASET_COLUMN] != self._dataset_id]
            df.to_parquet(parquet_file_path, index=False)
            ds_parquet = self._base_file_path[PARQUET_FILE]
            os.system(f'rm {ds_parquet}')
            rm_file_list.append(ds_parquet)

        pj_parquet_path = os.path.dirname(self._base_file_path[PARQUET_FILE])
        file_list = glob.glob(pj_parquet_path + '/*.parquet')
        if len(file_list) == 0:
            base_files = list(self._base_file_path.values())[1:]
            base_files.append(self._repo_parquet_file)
            os.system(f'rm {" ".join(base_files)}')
            rm_file_list += base_files
            self.feast_apply()

        return rm_file_list

    def feast_apply(self):
        """Define Feature View and feast apply."""
        for key, path in self._repo_path.items():
            # 각 속성들 저장해놓은 txt 파일 경로 호출.
            file_list = glob.glob(path+'/*.txt')
            # 속성별 Feature Store의 경로와 속성별 호출해야할 라이브러리 가져오기
            if key == FEATURE_VIEW:
                file_path = self._repo_fv_file
                import_libs = get_features_import_libs(self._ws_name)
            elif key == FILE_SOURCE:
                file_path = self._repo_sources_file
                import_libs = get_sources_import_libs()
            elif key == ENTITY:
                file_path = self._repo_entities_file
                import_libs = get_entities_import_libs()
            else:
                continue

            # 속성 내용들 저장.
            with open(file_path, 'w') as fs_file:
                fs_file.write(import_libs)
                for file_name in sorted(file_list):
                    with open(file_name, 'r') as f:
                        fs_file.write(f.read())
        # Feast apply
        os.system(f'feast -c {self._ws_feast_path} apply')
        return self._ws_feast_path

    def write_base_file(self):
        # base파일을 저장하는데, 있으면 그대로 두고 끝냄.
        # 그래서 parquet파일은 따로 저장해놓기때문에 self._base_file_path에서 PARQUET_FILE의 순서를 제일 처음으로 둬야함.
        if not os.path.exists(self._base_file_path[ENTITY]):
            with open(self._base_file_path[ENTITY], 'w', encoding='utf-8') as f:
                f.write(define_entity(self._pj_name, self._entity_name, self._entity_dtype))
            with open(self._base_file_path[FILE_SOURCE], 'w', encoding='utf-8') as f:
                f.write(define_file_source(self._pj_name, self._repo_parquet_file, self._timestamp_col))
            with open(self._base_file_path[FEATURE_VIEW], 'w', encoding='utf-8') as f:
                f.write(define_feature_view(self._pj_name, self._dataset_features))

class FeastServe(FeastRepo):
    def __init__(self, item: FeastServeItem):
        super().__init__(item)
        self._workspace_id = item.workspace_id
        self._project_id = item.project_id

        if item.bootstrap_servers is not None:
            self._bootstrap_servers = ','.join(item.bootstrap_servers)

        if item.input_data is not None:
            self._input_data = pd.DataFrame.from_dict(item.input_data)

        self._kafka_topic = f'project-{item.project_id}-response'
        self._feast_url = os.getenv('FEAST_URL')
        self._consumer_container_name = f'feast-consumer-{self._pj_name}'

    def serve(self):
        client = docker.from_env()
        container = client.containers.run(
            image='feast_consumer:0.1',
            detach=True,
            environment={
                'FEAST_URL': self._feast_url,
                'WORKSPACE_ID': self._workspace_id,
                'PROJECT_ID': self._project_id,
                'KAFKA_TOPIC': self._kafka_topic,
                'KAFKA_BOOTSTRAP_SERVERS': self._bootstrap_servers,
            },
            name=self._consumer_container_name,
            remove=True
        )
        return self._consumer_container_name

    def push(self):
        fs = FeatureStore(self._ws_feast_path)
        fs.write_to_offline_store(f'fv_{self._pj_name}', df=self._input_data)
        return "success"

    def shutdown(self):
        client = docker.from_env()
        con = client.containers.list(filters={'name':self._consumer_container_name})[0]
        return self._consumer_container_name

    def get_features(self):
        pass
