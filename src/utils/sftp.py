from pysftp import Connection, CnOpts


class SFTP:

    def __init__(self, sftp_server_config):
        self.server = sftp_server_config['host_address']
        self.username = sftp_server_config['user_name']
        self.private_key = sftp_server_config['key_path']
        self.sftp_folder = sftp_server_config['sftp_folder']
        self.connection_opts = CnOpts()
        self.connection_opts.hostkeys = None
        self.__connection: Connection = None

    def connect(self):
        if not self.__connection:
            self.__connection = Connection(self.server, self.username, self.private_key, cnopts=self.connection_opts)
        return self

    def put(self, file, remote_path):
        return self.__connection.put(file, remote_path)

    def remove(self, path):
        return self.__connection.remove(path)

    def rmdir(self, path):
        return self.__connection.rmdir(path)

    def listdir(self, path):
        return self.__connection.listdir(path)

    def is_dir(self, path):
        return self.__connection.isdir(path)

    def is_file(self, path):
        return self.__connection.isfile(path)

    def close(self):
        self.__connection.close()
        self.__connection = None
