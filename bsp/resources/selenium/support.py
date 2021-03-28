
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ElementIsFilled(object):
    """An expectation for checking that an element is filled.

    element_id - used to find the element
    """

    def __init__(self, element_id):
        self.element_id = element_id

    def __call__(self, driver):
        return driver.find_element_by_id(self.element_id).text != ""


def jquery_active(driver):
    """Check jQuery status."""
    return driver.execute_script('return jQuery.active;') == 0


def wait_until_ajax_finish(driver, timeout=10):
    """Wait ajax to finish."""
    wait = WebDriverWait(driver, timeout)
    wait.until(jquery_active)


def wait_until_element_is_filled(driver, element_id, timeout=10):
    """Wait element be filled."""
    wait = WebDriverWait(driver, timeout)
    wait.until(ElementIsFilled(element_id))


def wait_element_be_clickable(driver, css_element, timeout=10):
    """Wait element be clickable."""
    wait = WebDriverWait(driver, timeout)
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, css_element)
        )
    )


def wait_visibility_of_any_element(driver, css_element, timeout=10):
    """Wait any element be visible."""
    wait = WebDriverWait(driver, timeout)
    wait.until(
        EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, css_element)
        )
    )


def wait_until_visibility_of_element(driver, css_element, timeout=10):
    """Wait one element be visible."""
    wait = WebDriverWait(driver, timeout)
    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, css_element)
        )
    )


def wait_until_url_contains_a_text(driver, url, timeout=10):
    """Wait URL to be."""
    wait = WebDriverWait(driver, timeout)
    wait.until(
        EC.url_contains(url)
    )
