from ...utils.remoteexecuter.echo_client import send_command
from ..general import Log
from ..web.browser import Browser


class VideoRecording:

    host = None

    @classmethod
    def get_host(cls):
        if not cls.host:
            cls.host = Browser().get_node_id()
        return cls.host

    @classmethod
    def start_video(cls):
        start_command = "ffmpeg -f x11grab -r 25 -s 1360x1020 -i :99.0 -vcodec libx264"
        Log.info("Starting video recording with command: %s. Host: %s" % (start_command, cls.get_host()))
        send_command("START_VIDEO '%s'" % start_command, host=cls.get_host())

    @classmethod
    def stop_video(cls):
        stop_command = "pkill -INT ffmpeg"
        Log.info("Stopping video recording by command: %s" % stop_command)
        send_command("STOP_VIDEO '%s'" % stop_command, host=cls.get_host())

    @classmethod
    def get_video(cls, video_file):
        Log.info("Pulling video file: %s" % video_file)
        send_command("GET_VIDEO", host=cls.get_host(), respond_video_file=video_file)
