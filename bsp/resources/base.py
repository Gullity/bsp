import requests
from decouple import config
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.color import Color

from bsp.resources.selenium.support import (
    wait_element_be_clickable,
    wait_until_ajax_finish,
    wait_until_element_is_filled,
    wait_until_visibility_of_element,
    wait_visibility_of_any_element,
)

WEBSITE_HOST = config('WEBSITE_HOST', default='http://localhost:8000')
REQUESTS_SESSION = requests.Session()


class BasePage(object):
    HOST = WEBSITE_HOST

    def go(self, **params):
        return self.client.get(self.make_url(**params))

    def make_url(self, path=None, **params):

        if not path:
            path = self.PATH

        if not path.endswith('/'):
            path += '/'

        return f'{self.HOST}{path.format(**params)}'

    def assert_equal(self, param1, param2):
        """Ensure both parameters are equal."""
        if param1 != param2:
            raise AssertionError(f"{param1} != {param2}")

        return True


class SeleniumPage(BasePage):
    WAIT_ELEMENT = None
    WAIT_TIMEOUT = 10

    def __init__(self, browser):
        self.client = browser

    def click_on_button_using_id(self, button_id):
        """Find the element using id and then click."""
        element = self.client.find_element_by_id(button_id)
        element.click()

    def click_on_button_using_css_selector(self, attribute_value):
        """Find the element using css selector and then click."""
        wait_until_visibility_of_element(self.client, attribute_value)

        element = self.client.find_element_by_css_selector(attribute_value)
        wait_element_be_clickable(
            self.client, attribute_value, self.WAIT_TIMEOUT
        )
        element.click()

    def click_on_button_executing_script(self, attribute_value):
        """Find the element using css selector but click using script."""
        element = self.client.find_element_by_css_selector(attribute_value)
        element = self.client.execute_script("arguments[0].click();", element)

    def close_the_current_window(self):
        """Close the current window."""
        self.client.close()

    def fill_element(self, element_id, value):
        """Receive element_id and value.

        The firt one is use to find the element
        the second one is use as value in the element.
        """
        element = self.client.find_element_by_id(element_id)
        element.send_keys(value)

    def fill_element_using_css_selector(self, custom_attribute, value):
        """Receive the css selector and value.

        The firt one is use to find the element
        the second one is use as value in the element.
        """
        element = self.client.find_element_by_css_selector(custom_attribute)
        element.send_keys(value)

    def find_element_using_id(self, attribute_value):
        """Find the element based on id."""
        element = self.client.find_element_by_id(attribute_value)
        return element

    def find_element_using_css_selector(self, custom_attribute):
        """Find the element based on css selector."""
        wait_until_visibility_of_element(self.client, custom_attribute)
        element = self.client.find_element_by_css_selector(custom_attribute)
        return element

    def find_elements_using_css_selector(self, custom_attribute):
        """Find the elements based on css selector."""
        wait_until_visibility_of_element(self.client, custom_attribute)
        return self.client.find_elements_by_css_selector(custom_attribute)

    def get_title(self):
        return self.client.title

    def get_the_current_url(self):
        """Return the current url."""
        element = self.client.current_url
        return element

    def go(self, **params):
        """Go to URL."""
        super().go(**params)

    def refresh_the_page(self):
        """Refresh page."""
        self.client.refresh()

    def hover_element(self, custom_attribute):
        """Use the commom actions to hover the mouse over an element."""
        element = self.client.find_element_by_css_selector(
            custom_attribute
        )

        hover = ActionChains(self.client).move_to_element(element)
        hover.perform()

    def quit(self):
        self.client.quit()
