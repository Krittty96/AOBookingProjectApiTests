import json

import pytest
import requests
import os
from dotenv import load_dotenv
from core.settings.environments import Environment
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts
import allure
import jsonschema

from core.clients.schemas.booking_details_schema import BOOKING_DETAILS_SCHEMA

load_dotenv()


class APIClient:
    def __init__(self):
        environments_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environments_str]
        except KeyError:
            raise ValueError(f'Unsupported environment value: {environments_str}')

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json'
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f'Unsupported environment value: {environment}')

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step('Ping API client'):
            url = f'{self.base_url}{Endpoints.PING_ENDPOINT}'
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 201, f'Expected status 201 but got {response.status_code}'
        return response.status_code

    def auth(self):
        with allure.step('Getting authenticate'):
            url = f'{self.base_url}{Endpoints.AUTH_ENDPOINT}'
            payload = {'username': Users.USERNAME, 'password': Users.PASSWORD}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        token = response.json().get('token')
        with allure.step('Updating headers with authorization'):
            self.session.headers.update({'Authorization': f'Bearer {token}'})


    def get_booking_by_id(self, booking_id):
        with allure.step(f'Получение ID брони: {booking_id}'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}'
            response=self.session.get(url)
        with allure.step('Проверка статус кода ответа'):
            assert response.status_code == 200, f'Ожидается статус код 200, получен : {response.status_code}'
        with allure.step('Получение и проверка содержимого ответа'):
            booking_data = response.json()
            jsonschema.validate(booking_data, BOOKING_DETAILS_SCHEMA)
        return booking_data
