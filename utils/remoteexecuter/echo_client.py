import logging
import os
import socket

buffer_size = 2048


def send_command(command, host=None, port=11111, respond_video_file=None):
    if host is None:
        host = socket.gethostname()
    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection_socket.connect((host, port))
        connection_socket.sendto(command.encode(), (host, port))
        if respond_video_file is not None:
            file_bytes = connection_socket.recv(buffer_size)
            if file_bytes:
                path = os.path.dirname(os.path.abspath(respond_video_file))
                if not os.path.exists(os.path.abspath(path)):
                    os.makedirs(path)
                video_respond_file = open(respond_video_file, 'wb')
                while file_bytes:
                    video_respond_file.write(file_bytes)
                    file_bytes = connection_socket.recv(buffer_size)
                video_respond_file.close()
        connection_socket.shutdown(socket.SHUT_WR)
        connection_socket.close()
    except Exception as e:
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(message)s')
        logging.error(e)
