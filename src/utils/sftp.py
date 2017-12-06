import pysftp


class SFTP:

    @staticmethod
    def get_connection(sftp_server_config):
        connection_options = pysftp.CnOpts()
        connection_options.hostkeys = None
        return pysftp.Connection(sftp_server_config['host_address'], username=sftp_server_config['user_name'], private_key=sftp_server_config['key_path'], cnopts=connection_options)

    @staticmethod
    def put_file(sftp_server_config, file, remote_path):
        connection = SFTP.get_connection(sftp_server_config)
        try:
            connection.put(file, remote_path)
        finally:
            connection.close()

    @staticmethod
    def remove_file(sftp_server_config, remote_file_path):
        connection = SFTP.get_connection(sftp_server_config)
        try:
            connection.remove(remote_file_path)
        finally:
            connection.close()
