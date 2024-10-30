import os
import pathlib
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# Set Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Optional: run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver without specifying the service path explicitly
driver = webdriver.Chrome(options=chrome_options)

class WebpageTests(unittest.TestCase):
    def test_title(self):
        driver.get(file_uri("counter.html"))
        self.assertEqual(driver.title, "Counter")

    def test_increase(self):
        driver.get(file_uri("counter.html"))
        increase = driver.find_element("id", "increase")
        increase.click()
        self.assertEqual(driver.find_element("tag name", "h1").text, "1")

    def test_decrease(self):
        driver.get(file_uri("counter.html"))
        decrease = driver.find_element("id", "decrease")
        decrease.click()
        self.assertEqual(driver.find_element("tag name", "h1").text, "-1")

    def test_multiple_increase(self):
        driver.get(file_uri("counter.html"))
