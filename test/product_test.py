import pytest
import json
import threading
import time
import os
from http import HTTPStatus
from products_db_sumulator.server import server
from requests import post, get, put, delete
from app import app
from test.config import CHECKER_SIMULATOR_URL,INSTANCE_ID,PRODUCT_DB_URL
from threading import Thread
from event_loop import event_loop
from test import product_test
# static variable
product_test.delay_response = ""

@pytest.fixture(scope="session", autouse=True)
def custom_setup():
    print(f"Start flask server")
    #start products DB simulator
    t1 = threading.Thread(target=start_product_db)
    t1.start()
    #start  checker simulator
    t2 = threading.Thread(target=start_checker_simulator)
    t2.start()
    yield print("Start of test")
    #stop checker simulator
    response = post(url=CHECKER_SIMULATOR_URL + "/shutdown")
    assert response.status_code == HTTPStatus.OK, print(f"response.status is {response.status_code}")
    #stop products DB simulator
    response = post(url=PRODUCT_DB_URL + "/shutdown")
    assert response.status_code == HTTPStatus.OK, print(f"response.status is {response.status_code}")
    t1.join()
    t2.join()
    print("End of test")

@pytest.fixture(scope="module", autouse=True)
def setup_test():
    yield print(f"Starting test")
    teardown_test()

def teardown_test():
    print(f"Ending test")

def start_product_db(host='0.0.0.0', port=5050):
    server.run(debug=False, host=host, port=port)

def start_checker_simulator(host='0.0.0.0', port=5000):
    Thread(target=event_loop.run_forever, daemon=True).start()
    app.run(debug=False, host=host, port=port)

def test_update_immediate_response():
    os.environ['IMMEDIATE_RESPONSE'] = 'approval'
    os.environ['DELAY_TIME_SECONDS'] = "0"
    data = {}
    response = put(url=CHECKER_SIMULATOR_URL + "/product/" + INSTANCE_ID, data=data)
    json_response = json.loads(response.text)
    assert response.status_code == HTTPStatus.ACCEPTED, print(f"response.status is {response.status_code}")
    assert json_response['message']['instanceid'] == INSTANCE_ID
    assert json_response['message']['response'] == "approval"

def test_update_delay_response():
    product_test.delay_response = None
    os.environ['IMMEDIATE_RESPONSE'] = 'disapproval'
    os.environ['DELAY_TIME_SECONDS'] = "3"
    os.environ['DELAYED_RESPONSE'] = 'approval'
    data = {}
    response = put(url=CHECKER_SIMULATOR_URL + "/product/" + INSTANCE_ID, data=data)
    json_response = json.loads(response.text)
    assert response.status_code == HTTPStatus.ACCEPTED, print(f"response.status is {response.status_code}")
    assert json_response['message']['instanceid'] == INSTANCE_ID
    assert json_response['message']['response'] == "disapproval"
    time.sleep(4)
    assert product_test.delay_response == "approval"

def test_delete_immediate_response():
    os.environ['IMMEDIATE_RESPONSE'] = 'approval'
    os.environ['DELAY_TIME_SECONDS'] = "0"
    data = {}
    response = delete(url=CHECKER_SIMULATOR_URL + "/product/" + INSTANCE_ID, data=data)
    json_response = json.loads(response.text)
    assert response.status_code == HTTPStatus.ACCEPTED, print(f"response.status is {response.status_code}")
    assert json_response['message']['instanceid'] == INSTANCE_ID
    assert json_response['message']['response'] == "approval"

def test_delete_delay_response():
    product_test.delay_response = None
    os.environ['IMMEDIATE_RESPONSE'] = 'disapproval'
    os.environ['DELAY_TIME_SECONDS'] = "3"
    os.environ['DELAYED_RESPONSE'] = 'approval'
    data = {}
    response = delete(url=CHECKER_SIMULATOR_URL + "/product/" + INSTANCE_ID, data=data)
    json_response = json.loads(response.text)
    assert response.status_code == HTTPStatus.ACCEPTED, print(f"response.status is {response.status_code}")
    assert json_response['message']['instanceid'] == INSTANCE_ID
    assert json_response['message']['response'] == "disapproval"
    time.sleep(4)
    assert product_test.delay_response == "approval"