import pymssql
import re
import log
from traceback import format_exc

log = log.log('log.txt', 'DEBUG')

class DBConnectionError(Exception):
    pass


class TWDB(object):
    def __init__(self):
        try:
            #try to connect
            self.connection = pymssql.connect(
                host='HOST',
                database='DB',
                user='USER',
                password='PASS'
            )
            self.cursor = self.connection.cursor(as_dict=True)
        except pymssql.DatabaseError, e:
            log.error("OperationalError: %s" % format_exc())
            raise e

    def __del__(self):
        try:
            self.connection.close()
        except Exception:
            pass  # do nothing if connection is lost
        return

    def query(self, sql, first=False):
        log.debug("Query: %s" % (sql))
        self.cursor.execute(sql)
        if first:
            results = self.cursor.fetchone()
        else:
            results = self.cursor.fetchall()
        log.debug(results)
        return results

    def commit(self, sql):
        log.debug("Commit: %s" % (sql))
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            log.error('Exception: %s' % e)
            raise e  # raise the same exception to keep all the info
        return

    def get_ticket_counters(self):
        sql = 'select * from BI..hackathonXI;'
        return self.query(sql)


        
