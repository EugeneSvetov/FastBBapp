import datetime
import requests
import random
import urllib3
from webapp.shablon import Base
import fastreport_cloud_sdk
from fastreport_cloud_sdk.rest import ApiException
from pprint import pprint


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


def get_api_keys():
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.ApiKeysApi(api_client)

        try:
            api_response = api_instance.api_keys_get_api_keys()
            # pprint(api_response)
            return api_response.api_keys
        except ApiException as e:
            print("Exception when calling ApiKeysApi->api_keys_get_api_keys: %s\n" % e)

def create_api_key(description: str, expired: datetime.date = datetime.datetime.today()):
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.ApiKeysApi(api_client)
        create_api_key_vm = fastreport_cloud_sdk.CreateApiKeyVM(description, expired)

        try:
            api_response = api_instance.api_keys_create_api_key(create_api_key_vm)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ApiKeysApi->api_keys_create_api_key: %s\n" % e)


def delete_api_key(key):
    b = Base('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()

    json = {
        "apiKey": key
    }

    response = requests.delete(f'{b._host}/api/manage/v1/ApiKeys', headers=headers, json=json)


    print(response.status_code)