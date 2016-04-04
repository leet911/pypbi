import psycopg2
from psycopg2.extras import RealDictCursor 

import log
from traceback import format_exc

log = log.log('log.txt', 'DEBUG')

class MSDPDB(object):
    def __init__(self):
        try:
            #try to connect
            self.connection = psycopg2.connect(
                cursor_factory=RealDictCursor,
                database='DB_NAME',
                host='HOST',
                port=5433,
                user='USER',
                password='PASS'
            )
            self.cursor = self.connection.cursor()
        except psycopg2.DatabaseError, e:
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
        self.connection.commit()
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

    def get_recent_adds(self, days=0):
        days = int(days)
        sql = '''
            select
                to_char(clock_timestamp(), 'YYYY-MM-DD HH24:MI:SS') as "StatusDate",
                u.f_unit_id as "UnitID",
                u.f_name as "UnitName",
                sum(case when s.f_start_date > current_date-%s then 1 else 0 end) as "NewSubsToday"
            from t_subscription s
            join t_product p 
                on p.f_product_pk = s.f_product_pk
            join t_unit u
                on u.f_unit_pk = p.f_unit_pk
            where s.f_start_date > current_date-%s
            group by u.f_unit_id, u.f_name;
            ''' %(days, days)
        return self.query(sql)
