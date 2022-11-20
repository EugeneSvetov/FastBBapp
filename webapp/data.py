import requests
import urllib3
from webapp.shablon import Base

TOKEN = 'kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy'
PROS = '6379fb4b5f620ebfce9a63e4'
USER_NAME = 'apikey'


class DataSources(Base):
    def __init__(self, username: str, token: str, sub_id: str, host: str):
        super().__init__(username, token, sub_id, host)

    def create_data_source(self, name: str = 'New',
                           connection_string: str = 'json=aHR0cHM6Ly9hcGkubnBvaW50LmlvLzZiMTU1ODU5YTU4MWI4MzQzYjI0',
                           connection_type: str = 'JSON'):
        headers, sub_id = self._config()
        json = {
            "name": name,
            "connectionString": connection_string,
            "subscriptionId": sub_id,
            "connectionType": connection_type
        }
        response = requests.post(f'{self._host}/api/data/v1/DataSources', headers=headers, json=json)
        return response.json()

    def get_all_data_sources(self):
        headers, sub_id = self._config()
        response = requests.get(f'{self._host}/api/data/v1/DataSources?take=100', headers=headers)
        return response.json()

    def _get_data_source_by_name(self, name: str):
        headers, sub_id = self._config()
        all_ds = self.get_all_data_sources().get('dataSources')
        current_ds = [i for i in all_ds if i.get('name') == name][0]
        response = requests.get(f'{self._host}/api/data/v1/DataSources/{current_ds.get("id")}', headers=headers)
        return response.json()

    def delete_ds(self, name: str):
        headers, sub_id = self._config()
        all_ds = self.get_all_data_sources().get('dataSources')
        current_ds = [i for i in all_ds if i.get('name') == name][0]
        response = requests.delete(f'{self._host}/api/data/v1/DataSources/{current_ds.get("id")}', headers=headers)
        return response

    def fetch_ds(self, name: str):
        headers, sub_id = self._config()
        all_ds = self.get_all_data_sources().get('dataSources')
        current_ds = [i for i in all_ds if i.get('name') == name][0]
        response = requests.get(f'{self._host}/api/data/v1/DataSources/{current_ds.get("id")}/fetch', headers=headers)
        return response

    def upd_connection_string(self, name_ds: str,
                              connection_string: str = 'null'):
        headers, sub_id = self._config()
        all_ds = self.get_all_data_sources().get('dataSources')
        current_ds = [i for i in all_ds if i.get('name') == name_ds][0]
        json = {
            "connectionString": connection_string
        }
        response = requests.put(f'{self._host}/api/data/v1/DataSources/{current_ds.get("id")}/ConnectionString',
                                headers=headers, json=json)
        return response.json()

    def rename_ds(self, name_current: str, new_name: str = 'TEST'):
        headers, sub_id = self._config()
        all_ds = self.get_all_data_sources().get('dataSources')
        current_ds = [i for i in all_ds if i.get('name') == name_current][0]
        json = {
            "name": new_name
        }
        response = requests.put(f'{self._host}/api/data/v1/DataSources/{current_ds.get("id")}/rename',
                                headers=headers, json=json)
        return response.json()
