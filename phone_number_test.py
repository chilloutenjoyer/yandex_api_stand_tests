import data
import sender_stand_request
def get_user_body(phone):
    current_body = data.user_body.copy()
    current_body["phone"] = phone
    return current_body
def pos_assert(phone):
    user_body = get_user_body(phone)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code==201
    assert user_response.json()["authToken"] !=""
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
    + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user)==1

    #Тест 1 
    def test_create_user_10_symbols_get_succes_response():
        pos_assert("+74441237887")