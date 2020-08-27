from kom_framework import kom_config
from kom_framework.src.drivers.drivers import Driver


class DriverManager:

    sessions = dict()

    @classmethod
    def __get_session_key(cls, page_object):
        return page_object.get_session_key()

    @classmethod
    def get_session(cls, page_object):
        if kom_config['multi_application_mode'] == 'True':
            session_key = cls.__get_session_key(page_object)
            return cls.sessions.get(session_key, None)
        elif cls.sessions.keys():
            return cls.sessions[next(iter(cls.sessions))]
        return None

    @classmethod
    def create_session(cls, page_object, extensions):
        session_key = cls.__get_session_key(page_object)
        cls.sessions[session_key] = Driver(extensions).create_session()
        return cls.sessions[session_key]

    @classmethod
    def destroy_session(cls, page_object):
        if kom_config['multi_application_mode'] == 'True':
            del cls.sessions[cls.__get_session_key(page_object)]
        else:
            cls.sessions.clear()
