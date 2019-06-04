from kom_framework.src.web.drivers.drivers import Driver


class DriverManager:

    sessions = dict()

    @classmethod
    def __get_session_key(cls, page_object):
        return page_object.get_session_key()

    @classmethod
    def get_session(cls, page_object):
        session_key = cls.__get_session_key(page_object)
        if session_key in cls.sessions.keys():
            return cls.sessions[session_key]
        return None

    @classmethod
    def create_session(cls, page_object, extensions):
        session_key = cls.__get_session_key(page_object)
        cls.sessions[session_key] = Driver(extensions).create_session()
        return cls.sessions[session_key]

    @classmethod
    def destroy_session(cls, page_object):
        del cls.sessions[cls.__get_session_key(page_object)]
