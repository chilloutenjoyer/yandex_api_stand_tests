import data
import sender_stand_request

def get_user_address(address):
    current_body = data.user_body.copy()
    current_body['address'] = address
    return current_body

def positive_assert(address):
    user_body = get_user_address(address)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 201
    assert response.json()['authToken'] != ''
    user_table_response = sender_stand_request.get_users_table()
    str_user = user_body['firstName'] + ',' + user_body['phone'] + ','\
    + user_body['address'] + ',,,' + response.json()['authToken']
    assert user_table_response.text.count(str_user) == 1

def negative_assert(address):
    user_body = get_user_address(address)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()['code'] == 400
    assert response.json()['message'] == "Адресс введен некорректно." \
        " Адрес может содержать только русские буквы, цифры и знаки препинания,"\
        " длина адреса не должна быть менее 5 и более 50 символов"

#Тест 1
def test_create_user_5_letters_address_get_success_response():
    positive_assert('Город')

#Тест 2
def test_create_user_6_letters_address_get_success_response():
    positive_assert('ГородГ')

#Тест 3
def test_create_user_49_letters_address_get_success_response():
    positive_assert('ГородГородГородГородГородГородГородГородГородГоро')

#Тест 4
def test_create_user_50_letters_adress_get_success_response():
    positive_assert('ГородГородГородГородГородГородГородГородГородГород')

#Тест 5
def test_create_user_allowed_symbols_in_addres_get_success_response():
    positive_assert('Город. Город,-1')

#Тест 6
def test_create_user_4_letters_address_get_error_response():
    negative_assert('Горо')

#Тест 7
def test_create_user_3_letters_address_get_error_response():
    negative_assert('Гор')

#Тест 8
def test_create_user_51_letters_address_get_error_response():
    negative_assert('ГородГородГородГородГородГородГородГородГородГородГ')

#Тест 9
def test_create_user_52_letters_address_get_error_response():
    negative_assert('ГородГородГородГородГородГородГородГородГородГородГо')

#Тест 10
def test_create_user_english_letters_address_get_error_response():
    negative_assert('Gorod')

#Тест 11
def test_create_user_unallowed_symbols_get_error_response():
    negative_assert('Город№!";%')

#Тест 12
def test_create_user_no_address_get_error_response():
    user_body=data.user_body.copy()
    user_body['address'] = ''
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()['code'] == 400
    assert response.json()['message'] == "Не все необходимые параметры были переданы"

#Тест 13
def test_create_user_wrong_param_in_address_get_error_response():
    user_body= get_user_address(123456)
    response= sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()['code'] == 400