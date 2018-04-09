from ...web import multi_application_mode
from ...web.browser import Browser


class WebSessionsFactory:

    sessions = dict()
    active_module = None
    active_page = None
    active_frame = None

    @classmethod
    def browser(cls, module_name=None):
        if not multi_application_mode:
                module_name = "standard_mode"
        if module_name not in cls.sessions.keys():
            cls.sessions[module_name] = Browser(module_name)
        return cls.sessions[module_name]

    @classmethod
    def close_sessions(cls):
        for session in cls.sessions.keys():
            cls.sessions[session].quit()

    @classmethod
    def refresh_browsers(cls):
        for session in cls.sessions.keys():
            cls.sessions[session].refresh()

    @classmethod
    def get_browsers_log(cls):
        out = dict()
        for session in cls.sessions.keys():
            session_logs = cls.sessions[session].get_browser_log()
            out[session] = '\n'.join(session_logs)
        return out

    @classmethod
    def clear_browsers_local_storage(cls):
        for session in cls.sessions.keys():
            cls.sessions[session].clear_local_storage()
