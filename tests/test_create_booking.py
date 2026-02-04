import allure
import pytest
import requests
import jsonschema
from conftest import generate_random_booking_data
from core.clients.schemas.booking_details_schema import BOOKING_DETAILS_SCHEMA
from core.clients.api_client import Endpoints


@allure.feature("Test create booking")
@allure.story("Validate response")
def test_validate_response(api_client, generate_random_booking_data):
    url = f'{api_client.base_url}{Endpoints.BOOKING_ENDPOINT.value}'
    booking_data = generate_random_booking_data.copy()
    response = requests.post(url, json=booking_data)
    assert response.status_code == 200, f'Expected status code 200 , got {response.status_code}'
    response_data = response.json()
    with allure.step('JSON schema validation'):
        jsonschema.validate(instance=response_data, schema=BOOKING_DETAILS_SCHEMA)
    with allure.step("Verify response fields"):
        booking_details = response_data['booking']
        assert booking_details['firstname'] == booking_data['firstname'], f"Firstname mismatch: expected {response_data['firstname']}, got {booking_data['firstname']}"
        assert booking_details['lastname'] == booking_data['lastname'] , f"Firstname mismatch: expected {response_data['lastname']}, got {booking_data['lastname']}"
        assert booking_details['totalprice'] == booking_data['totalprice'] , f"Firstname mismatch: expected {response_data['totalprice']}, got {booking_data['totalprice']}"
        assert booking_details['depositpaid'] == booking_data['depositpaid'], f"Firstname mismatch: expected {response_data['depositpaid']}, got {booking_data['depositpaid']}"
        assert booking_details['bookingdates'] == booking_data['bookingdates'] , f"Firstname mismatch: expected {response_data['bookingdates']}, got {booking_data['bookingdates']}"
        assert booking_details['additionalneeds'] == booking_data["additionalneeds"], f"Firstname mismatch: expected {response_data['additionalneeds']}, got {booking_data['additionalneeds']}"


@allure.feature("Test create booking")
@allure.story("Test validate headers")
def test_validate_headers(api_client, generate_random_booking_data):
    url = f'{api_client.base_url}{Endpoints.BOOKING_ENDPOINT.value}'
    response = api_client.session.post(url, json=generate_random_booking_data.copy(),
                                       headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
    req_headers = response.request.headers
    assert "application/json" in req_headers.get('Content-Type')
    assert "application/json" in req_headers.get('Accept')
