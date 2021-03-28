import inspect
from importlib import import_module
from pathlib import Path

from decouple import config

__all__ = ['registry', 'get_resource', 'get_browser']


RESOURCES = {
    'SITE': {},
}


RESOURCES_DIR = Path(__file__).absolute().parent


def get_browser():
    selenium_driver = import_module(
        'bsp.resources.selenium.{}'.format(
            config('SELENIUM_DRIVER', default='chrome')
        )
    )

    return selenium_driver.browser()


def _list_modules(package):
    modules = []
    target_dir = RESOURCES_DIR / package

    for module in target_dir.iterdir():
        if not module.is_file() or module.name.startswith('_') or module.name.startswith('.'):
            continue

        name = module.name.replace(module.suffix, '')
        modules.append(f'bsp.resources.{package}.{name}')

    return modules


def _load_resources(category, *args, **kwargs):

    resources = {}

    for module_name in _list_modules(category):
        module = import_module(module_name)
        resources.update(
            {
                m[0]: m[1](*args, **kwargs)
                for m in inspect.getmembers(module, inspect.isclass)
                if m[1].__module__ == module_name
            }
        )

    return resources


def registry(browser):
    global RESOURCES

    RESOURCES['SITE'] = _load_resources('site', browser)


def get_resource(category, name):
    try:
        return RESOURCES[category.upper()][name]
    except KeyError:
        raise Exception(f'Resource {name} not found in {category} category')
