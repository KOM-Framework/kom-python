from kom_framework.src.web import multi_application_mode
from ...web.browser import Browser


class WebSessionsFactory:

    sessions = dict()
    session = None
    active_module = None
    active_page = None
    active_frame = None

    @classmethod
    def browser(cls, module_name):
        if multi_application_mode:
            if module_name not in cls.sessions.keys():
                cls.sessions[module_name] = Browser(module_name)
            return cls.sessions[module_name]
        elif not cls.session:
            cls.session = Browser()
        return cls.session

    @classmethod
    def close_sessions(cls):
        for session in cls.sessions.keys():
            cls.sessions[session].quit()
            cls.sessions.pop(session)

    @classmethod
    def refresh_browsers(cls):
        for session in cls.sessions.keys():
            cls.sessions[session].refresh()

    @classmethod
    def get_browsers_log(cls):
        out = dict()
        for session in cls.sessions.keys():
            session_logs = cls.sessions[session].get_browser_log()
            list_logs = list()
            for log_entry in session_logs:
                log_str = ''
                for key in log_entry.keys():
                    log_str += "%s: %s, " % (key, log_entry[key])
                list_logs.append(log_str)
            out[session] = '\n'.join(list_logs)
        return out

    @classmethod
    def clear_browsers_local_storage(cls):
        for session in cls.sessions.keys():
            cls.sessions[session].execute_script('window.localStorage.clear();')