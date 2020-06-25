import time
from datetime import datetime, timedelta

from pymysql import connect

from ..general import Log


class MySql:

    @staticmethod
    def execute_query(environment_configuration, query, wait_time=0):
        Log.info('Sending "%s" query to the "%s" database' % (query, environment_configuration['database']))
        start_time = datetime.now()
        rtn = []
        while True:
            conn = connect(user=environment_configuration['user'], password=environment_configuration['password'], host=environment_configuration['server'], database=environment_configuration['database'])
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            if (row and (row[0] is not None)) or (datetime.now() - start_time > timedelta(seconds=wait_time)):
                break
            conn.close()
            time.sleep(0.1)
        Log.info("Execution time = %s" % str(datetime.now() - start_time))
        while row:
            rtn.append(row)
            row = cursor.fetchone()
        query = query.lower()
        if query.startswith('update') or query.startswith('delete') or query.startswith('insert'):
            conn.commit()
        if query.startswith('insert'):
            rtn = cursor.lastrowid
        conn.close()
        return rtn

    @staticmethod
    def bulk_insert(environment_configuration, queries):
        Log.info('Using bulk insert into the database')
        out = list()
        conn = connect(user=environment_configuration['user'], password=environment_configuration['password'], host=environment_configuration['server'], database=environment_configuration['database'])
        cursor = conn.cursor()
        for query in queries:
            cursor.execute(query)
            out.append(cursor.lastrowid)
        conn.commit()
        conn.close()
        return out


class MySQLTable:

    @property
    def table_name(self):
        raise NotImplementedError

    @property
    def environment(self):
        raise NotImplementedError

    def update_column(self, column_name, value, condition):
        query = "UPDATE %s SET %s=%s WHERE %s" % (self.table_name, column_name, value, condition)
        MySql.execute_query(self.environment, query)

    def delete(self, condition=None):
        query = "DELETE FROM %s" % self.table_name
        if condition:
            query += " WHERE %s" % condition
        MySql.execute_query(self.environment, query)

    def select_value(self, column_name, condition, wait_time=1):
        query = "SELECT %s FROM %s WHERE %s" % (column_name, self.table_name, condition)
        value = MySql.execute_query(self.environment, query, wait_time)
        if not value:
            Log.info("SQl result is None")
            return None
        else:
            Log.info("SQl result: %s" % value[0][0])
            return value[0][0]

    def select_values(self, column_name, condition=None, wait_time=1):
        query = "SELECT %s FROM %s" % (column_name, self.table_name)
        if condition:
            query += ' WHERE %s' % condition
        values = MySql.execute_query(self.environment, query, wait_time)
        if values:
            values = [i[0] for i in values]
        Log.info("SQl result: %s" % values)
        return values

    def select_values_by_a_custom_condition(self, column_name, condition, wait_time=1):
        query = "SELECT %s FROM %s %s" % (column_name, self.table_name, condition)
        values = MySql.execute_query(self.environment, query, wait_time)
        if values:
            values = [i[0] for i in values]
        Log.info("SQl result: %s" % values)
        return values

    def prepare_queries_for_insert_from_dict(self, data):
        out_queries = list()
        for row in data:
            columns = list()
            values = list()
            for key in row.keys():
                columns.append(key)
                values.append(row[key])
            query = "INSERT INTO %s (%s) VALUE(%s)" % (self.table_name, ",".join(columns), ",".join(str(e) for e in values))
            out_queries.append(query)
        return out_queries

    def insert_values(self, column_values):
        query = self.prepare_queries_for_insert_from_dict([column_values])[0]
        out_id = MySql.execute_query(self.environment, query)
        return out_id

    def bulk_insert(self, data):
        queries = self.prepare_queries_for_insert_from_dict(data)
        ids = MySql.bulk_insert(self.environment, queries)
        return ids

    def delete_all_data(self):
        query = f'DELETE FROM {self.table_name}'
        return MySql.execute_query(self.environment, query)
