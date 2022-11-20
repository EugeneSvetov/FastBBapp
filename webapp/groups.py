from __future__ import print_function
import fastreport_cloud_sdk
import requests
from fastreport_cloud_sdk.rest import ApiException
from pprint import pprint
from webapp.shablon import Base


TOKEN='kfnsesp38bup97mijxauiwpdzubibh9ek1u7aq6f3u6w14s6sbgy'
PROS='6379fb4b5f620ebfce9a63e4'

def _config_api(token: str) -> fastreport_cloud_sdk.configuration.Configuration:
    configuration = fastreport_cloud_sdk.Configuration(
        host="https://fastreport.cloud",
        username='apikey',
        password=token,
    )
    return configuration

def get_subscription() -> fastreport_cloud_sdk.models.subscription_vm.SubscriptionVM:
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        a = fastreport_cloud_sdk.SubscriptionsApi(api_client)
        try:
            return a.subscriptions_get_subscription(id=PROS)
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_create_group: %s\n" % e)


def create_group(name: str):
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.GroupsApi(api_client)
        create_group_vm = fastreport_cloud_sdk.CreateGroupVM(name=name, subscription_id=PROS)

        try:
            api_response = api_instance.groups_create_group(create_group_vm=create_group_vm)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_create_group: %s\n" % e)


def _get_group(name: str = None) -> str:
    """Возвращает id группы с именем name"""
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.GroupsApi(api_client)
        skip = 0
        take = 10

        try:
            api_response = api_instance.groups_get_group_list(skip=skip, take=take)
            id = [i.id for i in api_response.groups if i.name == name]
            # print(api_response)
            return id
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_get_group_list: %s\n" % e)

def delete_group(group_id):
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.GroupsApi(api_client)
        try:
            api_instance.groups_delete_group(group_id)
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_delete_group: %s\n" % e)
def get_user_groups():
    b = Base('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()

    response = requests.get(f'{b._host}/api/manage/v1/Groups?take=100', headers=headers)
    return response.json().get('groups')


def update_name_group(new_name, group_id):
    b = Base('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()
    json = {
        'name': new_name
    }
    response = requests.put(f'{b._host}/api/manage/v1/Groups/{group_id}/rename', headers=headers, json=json)

    return response.json()


def all_users_in_current_group(group_id):
    b = Base('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()
    response = requests.get(f'{b._host}/api/manage/v1/Groups/{group_id}/Users?take=100', headers=headers)

    print(response.json())

def add_user_to_group(user_id, group_id):
    b = Base('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()
    response = requests.put(f'{b._host}/api/manage/v1/Groups/{group_id}/Users/{user_id}', headers=headers)

    print(response.status_code)

def remove_user_from_group(user_id, group_id):
    b = Base('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()
    response = requests.delete(f'{b._host}/api/manage/v1/Groups/{group_id}/Users/{user_id}', headers=headers)

    print(response.status_code)

def leave_from_group(group_id):
    b = Base('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()
    response = requests.delete(f'{b._host}/api/manage/v1/Groups/{group_id}/leave', headers=headers)

    print(response.status_code)