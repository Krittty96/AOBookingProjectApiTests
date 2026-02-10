import allure
import jsonschema
import pytest
from conftest import generate_random_booking_data
from core.clients.schemas.booking_details_schema import BOOKING_DETAILS_SCHEMA
from pydantic import ValidationError
from core.models.booking import BookingResponse
from core.clients.endpoints import Endpoints


@allure.feature("Test create booking")
@allure.story("Validate response")
def test_validate_response(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data.copy()
    response = api_client.create_booking(booking_data)
    with allure.step('JSON schema validation'):
        jsonschema.validate(instance=response, schema=BOOKING_DETAILS_SCHEMA)
    with allure.step("Verify response fields"):
        booking_details = response['booking']
        assert booking_details['firstname'] == booking_data[
            'firstname'], f"Firstname mismatch: expected {response['firstname']}, got {booking_data['firstname']}"
        assert booking_details['lastname'] == booking_data[
            'lastname'], f"Lastname mismatch: expected {response['lastname']}, got {booking_data['lastname']}"
        assert booking_details['totalprice'] == booking_data[
            'totalprice'], f"Totalprice mismatch: expected {response['totalprice']}, got {booking_data['totalprice']}"
        assert booking_details['depositpaid'] == booking_data[
            'depositpaid'], f"Depositpaid mismatch: expected {response['depositpaid']}, got {booking_data['depositpaid']}"
        assert booking_details['bookingdates'] == booking_data[
            'bookingdates'], f"Bookingdates mismatch: expected {response['bookingdates']}, got {booking_data['bookingdates']}"
        assert booking_details['additionalneeds'] == booking_data[
            "additionalneeds"], f"Additionalneeds mismatch: expected {response['additionalneeds']}, got {booking_data['additionalneeds']}"


@allure.feature("Test create booking")
@allure.story("Positive : creating booking with custom data")
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            'checkin': "2025-02-01",
            'checkout': "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature("Test create booking")
@allure.story("Positive : creating booking with random dates")
def test_create_booking_with_random_dates(api_client, generate_random_booking_data, booking_dates):
    booking_data = generate_random_booking_data.copy()
    booking_data['bookingdates'] = booking_dates
    response = api_client.create_booking(booking_data)
    assert response['booking']['bookingdates']['checkin'] == booking_dates['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_dates['checkout']

@allure.feature("Test create booking")
@allure.story("Checkin must to be before checkout")
def test_checkin_must_be_before_checkout(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data.copy()
    booking_data['bookingdates']['checkin'] = "2025-02-10"
    booking_data['bookingdates']['checkout'] = "2025-02-01"
    url = f'{api_client.base_url}{Endpoints.BOOKING_ENDPOINT.value}'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = api_client.session.post(url, json=booking_data, headers=headers)

    assert response.status_code >= 400 , 'Код ответа не соответствует ожидаемому'


