import allure
import jsonschema
from conftest import generate_random_booking_data
from core.clients.schemas.booking_details_schema import BOOKING_DETAILS_SCHEMA



@allure.feature("Test create booking")
@allure.story("Validate response")
def test_validate_response(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data.copy()
    response = api_client.create_booking(booking_data)
    with allure.step('JSON schema validation'):
        jsonschema.validate(instance=response, schema=BOOKING_DETAILS_SCHEMA)
    with allure.step("Verify response fields"):
        booking_details = response['booking']
        assert booking_details['firstname'] == booking_data['firstname'], f"Firstname mismatch: expected {response['firstname']}, got {booking_data['firstname']}"
        assert booking_details['lastname'] == booking_data['lastname'] , f"Firstname mismatch: expected {response['lastname']}, got {booking_data['lastname']}"
        assert booking_details['totalprice'] == booking_data['totalprice'] , f"Firstname mismatch: expected {response['totalprice']}, got {booking_data['totalprice']}"
        assert booking_details['depositpaid'] == booking_data['depositpaid'], f"Firstname mismatch: expected {response['depositpaid']}, got {booking_data['depositpaid']}"
        assert booking_details['bookingdates'] == booking_data['bookingdates'] , f"Firstname mismatch: expected {response['bookingdates']}, got {booking_data['bookingdates']}"
        assert booking_details['additionalneeds'] == booking_data["additionalneeds"], f"Firstname mismatch: expected {response['additionalneeds']}, got {booking_data['additionalneeds']}"


