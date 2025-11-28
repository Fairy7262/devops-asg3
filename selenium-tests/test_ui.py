from selenium import webdriver
from selenium.webdriver.common.by import By
import time, requests

BASE = "http://web:5000"

def test_homepage():
    r = requests.get(BASE)
    assert r.status_code == 200

