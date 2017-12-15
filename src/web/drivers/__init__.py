from ...web import browser
from . import drivers


driver = getattr(drivers, browser)
