import configuration
import data
import requests
def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.DATA_USER_PATH, json=body, headers=data.headers)
response = post_new_user(data.user_body)
def get_users_table():
    return requests.get(configuration.URL_SERVICE+configuration.USERS_PATH)