import data
import sender_stand_request

def get_user_body_phone(phone):
    current_body = data.user_body.copy()
    current_body["phone"] = phone
    return current_body

def pos_assert(phone):
    user_body = get_user_body_phone(phone)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code==201
    assert user_response.json()["authToken"] !=""
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
    + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user)==1

def neg_assert(phone):
    user_body = get_user_body_phone(phone)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json() ["message"] == "Телефонный номер пользователя введен некорреткно. " \
    "Номер может содержать только цифры и знак +"

def neg_assert_no_number(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

#Тест 1 
def test_create_10_symbols_in_number__get_succes_response():
    pos_assert("+744412378")

#Тест 2 
def test_create_11_symbols_in_number__get_succes_response():
    pos_assert("87444567853")

# Тест 3 
def test_create_12_symbols_in_number__get_succes_response():
    pos_assert("+74445678532")

# Тест 4 
def test_create_9_symbols_in_number__get_error_response():
    neg_assert("+12345678")

# Тест 5 
def test_create_8_symbols_in_number__get_error_response():
    neg_assert("+1234567")

#Тест 6
def test_create_1_symbols_in_number__get_error_response():
    neg_assert("+")

#Тест 7
def test_create_no_number_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("phone")
    neg_assert_no_number(user_body)

#Тест 8
def test_create_13_symbols_in_number_get_error_response():
    neg_assert("+744456785323")

#Тест 9
def test_create_14_symbols_get_error_response():
    neg_assert("+7444567853235")

#Тест 10 
def test_create_20_symbols_in_number_get_error_response():
    neg_assert("+7444567853235612345")

#Тест 11
def test_create_letters_in_number_get_error_response():
    neg_assert("+74445a78532")

#Тест 12 
def test_create_spacebar_in_number_get_error_response():
    neg_assert("+744 5678532")

#Тест 13 
def test_create_wrong_symbols_in_number_get_error_response():
    neg_assert("!@#$@#$!@#!@")

#Тест 14
def test_create_empty_param_in_number_get_error_response():
    user_body = data.user_body.copy()
    user_body["phone"] = ""
    neg_assert_no_number(user_body)

#Тест 15 
def test_create_wrong_param_type_in_number_get_error_response():
    user_body = get_user_body_phone(12345678901)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400