from kom_framework.src.base_element import KOMElementBase
from kom_framework.src.general import Log
from kom_framework.src.support.driver_aware import DriverAware


class ActionChainsMixin:

    def __init__(self, driver: DriverAware, element: KOMElementBase, element_name: str):
        self.action_chains = driver.action_chains
        self.element = element
        self.element_name = element_name

    def perform(self):
        Log.info('Performs all stored actions.')
        self.action_chains.perform()

    def reset_actions(self):
        Log.info('Clears actions that are already stored on the remote end.')
        self.action_chains.reset_actions()

    def click(self):
        Log.info('Clicks an "%s" element.' % self.element_name)
        return self.action_chains.click(self.element)

    def click_and_hold(self):
        Log.info('Holds down the left mouse button on an "%s" element.' % self.element_name)
        return self.action_chains.click_and_hold(self.element)

    def context_click(self):
        Log.info('Performs a context-click (right click) on an %s element.' % self.element_name)
        return self.action_chains.context_click(self.element)

    def double_click(self):
        Log.info('Double-clicks an "%s" element.' % self.element_name)
        return self.action_chains.double_click(self.element)

    def drag_and_drop(self, destination: KOMElementBase):
        Log.info('Holds down the left mouse button on the source "%s" element'
                 'then moves to the "%s" target element and releases the mouse button.'
                 % (self.element_name, destination.name))
        return self.action_chains.drag_and_drop(self.element, destination.find())

    def drag_and_drop_by_offset(self, xoffset, yoffset):
        Log.info('Holds down the left mouse button on the source element "%s", then moves to the target offset and '
                 'releases the mouse button.' % self.element_name)
        return self.action_chains.drag_and_drop_by_offset(self.element, xoffset, yoffset)

    def key_down(self, value):
        Log.info('Sends a key press only, without releasing it')
        return self.action_chains.key_down(value, self.element)

    def key_up(self, value):
        Log.info('Releases a modifier key.')
        return self.action_chains.key_up(value, self.element)

    def move_by_offset(self, xoffset, yoffset):
        Log.info('Moving the mouse to an offset from current mouse position.')
        return self.action_chains.move_by_offset(xoffset, yoffset)

    def move_to_element(self):
        Log.info('Moving the mouse to the middle of an "%s" element.' % self.element_name)
        return self.action_chains.move_to_element(self.element)

    def move_to_element_with_offset(self, xoffset, yoffset):
        Log.info('Move the mouse by an offset of the specified "%s" element.' % self.element_name)
        return self.action_chains.move_to_element_with_offset(self.element, xoffset, yoffset)

    def pause(self, seconds):
        Log.info('Pause all inputs for the specified duration in seconds')
        return self.action_chains.pause(seconds)

    def release(self):
        Log.info('Releasing a held mouse button on an "%s" element.' % self.element_name)
        return self.action_chains.release(self.element)

    def send_keys(self, *keys_to_send):
        Log.info('Sends keys to current focused element.')
        return self.action_chains.send_keys(keys_to_send)

    def send_keys_to_element(self, *keys_to_send):
        Log.info('Sends keys to an "%s" element.' % self.element_name)
        return self.action_chains.send_keys_to_element(self.element, keys_to_send)
