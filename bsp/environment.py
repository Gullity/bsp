from bsp.resources.base import (
    BasePage,
    SeleniumPage
)

from bsp.resources.loader import (
    get_browser,
    get_resource,
    registry
)


browser = get_browser()


def before_all(context):
    registry(browser)

def after_all(context):
    SeleniumPage(browser).quit()

def before_scenario(context, scenario):
    name = scenario.filename.split('/')[-1].replace('.feature', '').capitalize()
    context.me = get_resource('SITE', name)