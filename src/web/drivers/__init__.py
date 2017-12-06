from kom_framework.src.web import browser
from . import drivers


driver = getattr(drivers, browser)
