import pytest
import asyncio
import json
from requestHandlers import loginRequest, makePatientRequest
import aiohttp
    
def test_login_valid():
        email = "test@ipmedth.nl"
        password = "welkom1234"
        status, res = asyncio.run(loginRequest(email, password))
        assert status == "Ok", "Test Failed"
        # assert status != "Ok", "test_login_valid: Failed"
    
def test_login_invalid():
    email = "top@ipmedth.nl"
    password = "welkom1434"
    status, res = asyncio.run(loginRequest(email, password))
    assert status == "Failed", "Test Failed"
    
def test_new_patient_valid():
    token_type = "Bearer"
    token = "19|HwaLfTS0WFBmr3f8bRxlR4DvZyUlOKRXI3esR3HM"
    name = "Unit Test"
    email = "unittest11@ipmedth.nl"
    date = "2022-01-01"
    status, res = asyncio.run(makePatientRequest(token_type, token, name, email, date))
    assert status == "Ok", "Test Failed"
    
def test_new_patient_invalid():
    token_type = "Bearer"
    token = "19|HwaLfTS0WFBmr3f8bRxlR4DvZyUlOKRXI3esR3HM"
    name = ""
    email = "unittest10@ipmedth.nl"
    date = "2022-01-01"
    status, res = asyncio.run(makePatientRequest(token_type, token, name, email, date))
    assert status == "Failed", "Test Failed"
    
if __name__ == '__main__':
    pytest.main(['--no-header', '-v'])