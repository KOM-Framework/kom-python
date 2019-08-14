import csv
import logging
import os
import random
import string
import json
import time

from datetime import datetime
from subprocess import check_call

import re


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance


class Log:

    filename = None
    logger = logging.getLogger("KOM")

    @classmethod
    def get_logger(cls):
        if len(cls.logger.handlers) == 0:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
            handler.setLevel(logging.DEBUG)
            cls.logger.addHandler(handler)
            cls.logger.setLevel(logging.DEBUG)

            cls.filename = os.path.join(os.path.join(os.getcwd(), f"test{os.sep}logs{os.sep}"),
                                        datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S") + '.log')
            if not os.path.exists(os.path.dirname(cls.filename)):
                os.makedirs(os.path.dirname(cls.filename))
            fh = logging.FileHandler(cls.filename)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
            fh.setFormatter(formatter)
            cls.logger.addHandler(fh)
        return cls.logger

    @classmethod
    def info(cls, message):
        cls.get_logger().info(message)

    @classmethod
    def debug(cls, message):
        cls.get_logger().debug(message)

    @classmethod
    def error(cls, message):
        cls.get_logger().error(message)

    @classmethod
    def warning(cls, message):
        cls.get_logger().warning(message)


class JSONReader:

    @staticmethod
    def get_data_from_json(file_path, section, index, key):
        file = os.path.join(os.path.dirname(__file__), file_path)
        with open(file) as data_file:
            data = json.load(data_file)
            out_data = data[section]
            if index is not None:
                out_data = out_data[index]
            if key is not None:
                out_data = out_data[key]
            return out_data

    @staticmethod
    def get_data(section, key=None, index=0, file=""):
        out = JSONReader.get_data_from_json(file, section, index, key)
        if key == 'logo_image':
            root = os.path.dirname(__file__)
            logo = os.path.abspath(os.path.join(root, out))
            return logo
        return out

    @staticmethod
    def get_data_from_string(section, key=None, index=0, json_string=None):
        if json_string is not None:
            data = json.loads(json_string)
            out_data = data[section]
            if index is not None:
                out_data = out_data[index]
            if key is not None:
                out_data = out_data[key]
            return out_data
        return None


class Vars:
    # Dynamic variables storage

    variables = dict()

    @classmethod
    def __setattr__(cls, attr, value):
        cls.variables[attr] = value

    @classmethod
    def __getattr__(cls, attr):
        if attr not in cls.variables:
            raise AttributeError
        out = cls.variables[attr]
        return out

    @classmethod
    def exists(cls, var_name):
        keys = cls.variables.keys()
        return var_name in keys


def find_between(str_in, first, last):
    try:
        start = str_in.index(first) + len(first)
        if last == '':
            end = len(str_in)
        else:
            end = str_in.index(last, start)
        return str_in[start:end]
    except ValueError:
        return None


class File:

    @staticmethod
    def wait_until_file_download_finish(file_path=None, directory=None, regex=None, wait_time=5):
        end_time = time.time() + wait_time
        if file_path:
            while not os.path.exists(file_path) and time.time() < end_time:
                time.sleep(1)
            return os.path.isfile(file_path)
        elif directory and regex:
            file_path = None
            while not file_path and time.time() < end_time:
                time.sleep(1)
                file_path = File.get_file_by_regex(directory, regex)
            if file_path:
                return os.path.abspath(os.path.join(directory, file_path))

    @staticmethod
    def get_file_by_regex(dir_name, regex):
        """
            find the first file in the input - directory with name matching regular expression of input - regex.
            return the name of the file found
        """
        pattern = re.compile(regex)
        for filename in os.listdir(dir_name):
            if pattern.match(filename):
                return filename


class Random:

    @staticmethod
    def rand_char_string(length):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    @staticmethod
    def rand_int_string(length):
        return ''.join(random.choice(string.digits) for _ in range(length))


def create_csv_data_file(file, data):
    with open(file, 'w', newline='') as csv_file:
        spamwriter = csv.writer(csv_file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            spamwriter.writerow(['"%s"' % item for item in row])
        csv_file.close()


def make_gzip_archive(file):
    compressed_file_path = os.path.basename(file) + '.gz'
    try:
        os.remove(compressed_file_path)
    except OSError:
        pass
    check_call(['gzip', file])
    return compressed_file_path


def get_obj_key(obj_cls, *args, **kwargs):
    return str(obj_cls) + str(args) + str(kwargs)
