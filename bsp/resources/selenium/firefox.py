from pathlib import Path
from decouple import config

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


user = config('REMOTE_USER', default='')
key = config('REMOTE_PASSWORD', default='')
host = config('REMOTE_HOST', default='')


def browser():
    """Firefox Browser."""
    if config('USE_REMOTE', cast=bool, default=False):
        caps = {}

        return webdriver.Remote(
            command_executor=f'https://{host}/wd/hub',
            desired_capabilities=caps
        )

    options = Options()
    options.add_argument('--window-size=1200,2400')
    project_path = Path(__file__).absolute().parent.parent.parent.parent
    executable_path = str(
        project_path / 'external' / 'selenium' / 'geckodriver'
    )

    if config("USE_HEADLESS_BROWSER", cast=bool, default=False):
        options.add_argument('headless')

    return webdriver.Chrome(executable_path, chrome_options=options)