import requests
import urllib3

TOKEN = 'yuptozbh36s5uj1qkojexo5w91snjjmcw3sya8s84zy8t8yjow9y'
PROS = '6377865f5f620ebfce9a07ce'
USER_NAME = 'apikey'


class Base:
    def __init__(self, username: str, token: str, sub_id: str, host: str):
        self._username = username
        self._token = token
        self._sub_id = sub_id
        self._host = host

    def _config(self):
        auth = urllib3.util.make_headers(
            basic_auth=self._username + ':' + self._token
        ).get('authorization')

        headers = {
            'accept': 'application/json',
            'Authorization': auth,
            'Content-Type': 'application/json-patch+json'
        }
        return headers, self._sub_id


class Exports(Base):
    def __init__(self, username: str, token: str, sub_id: str, host: str):
        super().__init__(username, token, sub_id, host)

    def _get_root_folder(self):
        headers, sub_id = self._config()
        response = requests.get(f'{self._host}/api/rp/v1/Exports/Root?subscriptionId={PROS}', headers=headers).json()
        return response

    def get_count(self):
        headers, sub_id = self._config()
        response = requests.get(f'{self._host}/api/rp/v1/Exports/Folder/6377865f5f620ebfce9a07cd/CountFolderAndFiles', headers=headers)
        return response.json()

    def get_folder(self, name: str):
        headers, sub_id = self._config()
        root = self._get_root_folder()
        print(root.get('id'))
        folder_and_files = requests.get(f'{self._host}/api/rp/v1/Exports/Folder/{root.get("id")}/ListFolderAndFiles',
                                        headers=headers).json()

        return [i for i in folder_and_files.get('files') if i.get('name') == name][0]

    def _get_list_folders(self, name: str = 'root'):
        headers, sub_id = self._config()
        folder = self._get_root_folder() if name == 'root' else self.get_folder(name)
        list_folder = requests.get(f'{self._host}/api/rp/v1/Exports/Folder/{folder.get("id")}/ListFolders',
                                   headers=headers).json()
        return (list_folder.get('files'))

    def _get_list_files_folder(self, name: str = 'root'):
        tem = Exports('apikey', 'yuptozbh36s5uj1qkojexo5w91snjjmcw3sya8s84zy8t8yjow9y', '6377865f5f620ebfce9a07ce',
                        'https://fastreport.cloud')
        headers, sub_id = self._config()
        folder = self._get_root_folder() if name == 'root' else self.get_folder(name)
        list_folder = requests.get(
            f'{self._host}/api/rp/v1/Exports/Folder/{folder.get("id")}/ListFolderAndFiles?take={tem.get_count()["count"]}',
            headers=headers).json()
        return list_folder.get('files')

    def create_folder(self, parent_name: str = 'root'):
        headers, sub_id = self._config()
        folder = self._get_root_folder() if parent_name == 'root' else self.get_folder(parent_name)
        json_folder = {
            "name": 'New_Folder',
            "tags": [
                'null'
            ],
            "icon": 'null'
        }
        new_folder = requests.post(f'{self._host}/api/rp/v1/Exports/Folder/{folder.get("id")}/Folder',
                                   headers=headers, json=json_folder).json()
        return new_folder

    def delete_folder(self, name: str):
        headers, sub_id = self._config()
        folder = self.get_folder(name)
        del_folder = requests.delete(f'{self._host}/api/rp/v1/Exports/Folder/{folder.get("id")}/ToBin',
                                     headers=headers)
        return del_folder

    def delete_file(self, name: str):
        headers, sub_id = self._config()
        file = self._get_file_by_name(name)
        del_folder = requests.delete(f'{self._host}/api/rp/v1/Exports/File/{file.get("id")}/ToBin',
                                     headers=headers)
        return del_folder

    def create_file(self, folder_name: str = 'root'):
        headers, sub_id = self._config()
        folder = self._get_root_folder() if folder_name == 'root' else self.get_folder(folder_name)
        json = {
            "name": 'new',
            "content": 'null'
        }
        file = requests.post(f'{self._host}/api/rp/v1/Exports/Folder/{folder.get("id")}/File', headers=headers,
                             json=json)
        return print(file.json())

    def _get_file_by_name(self, name: str, folder_name: str = 'root'):
        headers, sub_id = self._config()
        folder = self._get_root_folder() if folder_name == 'root' else self.get_folder(folder_name)
        response = requests.get(f'{self._host}/api/rp/v1/Exports/Folder/{folder.get("id")}/ListFiles?take=100',
                                headers=headers).json()
        return [i for i in response.get('files') if i.get('name') == f'{name}'][0]

    def prepare_file(self, file_name: str, folder_name: str = 'root', file_prepare_name: str = None):
        headers, sub_id = self._config()
        file = self._get_file_by_name(file_name, folder_name)
        json = {
            "name": file_prepare_name,
            "pagesCount": 2147483647
        }
        lol = requests.post(f'{self._host}/api/rp/v1/Exports/File/{file.get("id")}/Prepare', headers=headers,
                            json=json)
        print(lol.json())

    def _get_root_reports_dir(self):
        headers, sub_id = self._config()
        response = requests.get(f'{self._host}/api/rp/v1/Reports/Root', headers=headers)
        return response.json()

    def _get_files_list_rep(self, folder_name: str = 'root'):
        headers, sub_id = self._config()
        folder = self._get_root_reports_dir() if folder_name == 'root' else self.get_folder(folder_name)
        response = requests.get(f'{self._host}/api/rp/v1/Reports/Folder/6377865f5f620ebfce9a07cc/ListFiles?take=100',
                                headers=headers)
        return response.json()

    def _get_file_rep(self, name: str, folder_name: str = 'root'):
        headers, sub_id = self._config()
        files = self._get_files_list_rep(folder_name=folder_name)
        file = [i for i in files.get('files') if i.get("name") == f'{name}.fpx'][0]
        response = requests.get(f'{self._host}/api/rp/v1/Reports/File/{file.get("id")}', headers=headers)
        return response.json()

    def export_file(self, file_name: str, format: str, folder_name: str = 'root', export_name: str = None):
        headers, sub_id = self._config()
        json = {
            "fileName": export_name,
            "pagesCount": 2147483647,
            "format": format
        }
        fileq = self._get_file_rep(file_name, folder_name=folder_name)
        print(fileq)
        file = requests.post(f'{self._host}/api/rp/v1/Exports/File/{fileq.get("templateId")}/Export', headers=headers,
                             json=json)
        return file.json()

    def download_file(self, file_name: str):
        headers, sub_id = self._config()
        root_id = requests.get(f'{self._host}/api/rp/v1/Exports/Root', headers=headers).json().get('id')
        files = requests.get(f'{self._host}/api/rp/v1/Exports/Folder/{root_id}/ListFiles?take=100', headers=headers).json()
        file = [i for i in files.get('files') if i.get('name') == file_name][0]
        response = requests.get(f'{self._host}/download/e/{file.get("id")}', headers=headers)
        wer = requests.get(response.url, headers=headers)
        print(wer.content)

        with open(f'{file_name}', 'wb') as f:
            f.write(wer.content)

# ex = Exports('apikey', 'yuptozbh36s5uj1qkojexo5w91snjjmcw3sya8s84zy8t8yjow9y', '6377865f5f620ebfce9a07ce', 'https://fastreport.cloud')
# print(ex._get_root_folder())