from kom_framework.src.web.data_types import Locator
from kom_framework.src.web.data_types.element_list_types import SelectList
from kom_framework.src.web.data_types.element_types import TextBlock, Button, Link


class PageElementFactory:
    def __init__(self, ancestor):
        self.ancestor = ancestor

    def text_block(self, locator: Locator, **kwargs) -> TextBlock:
        return TextBlock(self, locator, **kwargs)

    def button(self, locator: Locator, **kwargs) -> Button:
        return Button(self, locator, **kwargs)

    def link(self, locator: Locator, **kwargs) -> Link:
        return Link(self, locator, **kwargs)

    def select_list(self, locator: Locator, option_list_locator=None, message_locator=None,
                    extent_list_by_click_on_field=True, hide_list_by_click_on_field=False,
                    **kwargs) -> SelectList:
        return SelectList(self, locator, option_list_locator, message_locator, extent_list_by_click_on_field,
                          hide_list_by_click_on_field, **kwargs)
