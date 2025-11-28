import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "http://web:5000"

def test_full_message_flow():
    # 1. Backend reachable
    r = requests.get(BASE)
    assert r.status_code == 200

    # 2. Start Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Remote(
        command_executor="http://chrome:4444/wd/hub",
        options=options
    )

    try:
        # 3. Open homepage
        driver.get(BASE)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        # Verify heading
        heading = driver.find_element(By.TAG_NAME, "h1").text
        assert "Message App" in heading or "Simple Message App" in heading

        # 4. Submit a new message
        msg_box = driver.find_element(By.NAME, "msg")
        test_message = f"selenium-advanced-{int(time.time())}"
        msg_box.send_keys(test_message)

        driver.find_element(By.TAG_NAME, "button").click()

        # Give backend a second to write into DB
        time.sleep(1)

        # 5. Reload page and verify message in list
        driver.get(BASE)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "li"))
        )
        items = [i.text for i in driver.find_elements(By.TAG_NAME, "li")]

        assert test_message in items, "Submitted message not found in list!"

        # 6. Ensure no UI crashes
        assert "error" not in driver.page_source.lower()

    finally:
        driver.quit()
