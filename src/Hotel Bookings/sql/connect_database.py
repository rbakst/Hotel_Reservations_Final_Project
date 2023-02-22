import pyodbc
import sqlalchemy
import pandas as pd
import logging
from sqlalchemy.orm import sessionmaker
import sys
#Inside of Automation_pc_folder must sit db_info.py file with the db information needed to connect to the db
#sys.path.append(an.AFM_pc_folder)
#s_path = MAPPING_TOOLS_FOLDER + '/'+ s_file
#sys.path.append(an.DB_INFO_FOLDER)
import sql.db_info as db_info #this file has the dbinfo:server,db,user,pass,etc.
#This class is to connect to the database
class DbCon:
    def __init__(self):
            self.m_sServer = db_info.server
            self.m_sDriver = db_info.driver
            self.m_sDb = db_info.database
            self.m_sUsername = db_info.username
            self.m_sPassword = db_info.password
            self.m_bConnected = False
    def Connect(self):
        # self.m_oConn = pyodbc.connect('Driver='+self.m_sDriver+';'
        #               'Server=tcp:'+self.m_sServer+';'
        #               'Database='+self.m_sDb+';'
        #               'UID='+self.m_sUsername+';'
        #               'PWD='+ self.m_sPassword+';'
        #               #'ENCRYPT=yes;'
        #               #'Trusted_Connection=Yes;'
        #               'CONNECTION TIMEOUT=30;',
        #               #autocommit=True
        #               )
        #engine = sa.create_engine('mssql+pyodbc://user:password@server/database')
        'mssql://*server_name*/*database_name*?trusted_connection=yes'
        s = 'mssql+pyodbc://' + self.m_sServer + '/'+ self.m_sDb + '?driver='+ self.m_sDriver + '&trusted_connection=yes'
        s = 'mssql+pyodbc://@' + self.m_sServer + '/' + self.m_sDb + '?trusted_connection=yes&driver='+self.m_sDriver
        self.m_engine = sqlalchemy.create_engine(s)
        #engine = sqlalchemy.create_engine('mssql+pyodbc://{}/{}?driver={}'.format(self.m_sServer, self.m_sDb, driver))
        self.m_oConn = self.m_engine.raw_connection()
        #self.m_oSession = Session(sessionmaker(bind=self.m_engine,autocommit=False))
        Session = sessionmaker(bind=self.m_engine,autocommit=False)
        self.m_oSession = Session()
        self.m_bConnected = True
    def Disconnect(self):
        if self.m_bConnected:
            self.m_oConn.cursor().close()
            self.m_oSession.close_all()
            self.m_engine.dispose()
            self.m_oConn.close()
            self.m_bConnected = False
    def ReadSqlQuery(self, sQuery):
        if (self.m_bConnected == False):
            print('Error: db found disconnected and will try to connect again while tryng to run a query')
            self.Connect()
            if (self.m_bConnected == False):
                print('Error: db disconnected while tryng to run a query')
        df = pd.read_sql_query(sQuery,self.m_engine)
        return df
    def  insert_record(self, sql, val = None):
        '''format needed:
            sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
            val = ("John", "Highway 21")
            when ready call #self.m_oCursor.commit()
        '''
        o_cursor = self.m_oConn.cursor()
        #o_cursor.fast_executemany = True
        o_cursor.execute(sql)
        logging.debug(o_cursor.rowcount, "record inserted.")
        if o_cursor.rowcount < 1:
            logging.debug('inserted less than 1 row for sql: ' + sql)
        return o_cursor.rowcount
    def  update_records(self, sql, val = None):
        '''
            updates records and returns amount updated
            when ready call #self.m_oCursor.commit()
        '''
        o_cursor = self.m_oConn.cursor()
        o_cursor.execute(sql)
        logging.debug(o_cursor.rowcount, "records updated.")
        return o_cursor.rowcount
    def  delete_records(self, sql, b_commit = True):
        '''
            updates records and returns amount updated
            when ready call #self.m_oCursor.commit()
        '''
        o_cursor = self.m_oConn.cursor()
        o_cursor.execute(sql)
        logging.debug(o_cursor.rowcount, "records deleted (from parent table).")
        if b_commit:
            self.m_oConn.commit()
        return o_cursor.rowcount
    def insert_df(self, df_to_insert, s_table_name):
        #__init__() got multiple values for argument 'schema'
        df_to_insert.to_sql(s_table_name, con=self.m_engine, if_exists='append', index=False, chunksize=1000) #,
        self.m_oCursor.commit()
    #To do need to figure out how to get back the ids of rmq correspodning to the residents
    #If stuck insert with a loop?
    #It seems I am getting it back, try it with more residents
    #use in sql: OUTPUT INSERTED.id
    #now not using:
    def  insert_record_getting_id(self, sql, n_id_total = 1):
        '''format needed:
            sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
            val = ("John", "Highway 21")
            when ready call #self.m_oCursor.commit()
        '''
        o_cursor = self.m_oConn.cursor()
        result = o_cursor.execute(sql)
        s = result.fetchmany()[0]
        #need to add:
        #OUTPUT INSERTED.id into @id_scope see https://stackoverflow.com/questions/43358929/how-to-get-multiple-scope-identity-from-table-then-insert-to-other-table
        id = o_cursor.execute('SELECT SCOPE_IDENTITY()').fetchmany()[0]
        #have to be careful, no multi threading, otherwise make sure that sql statement returns id:
        #select scope identity only returns the last one
        ls_ids = []
        for i in range (n_id_total):
            id = o_cursor.execute('SELECT SCOPE_IDENTITY()').fetchone()[0]
            n_id = int(id)
            ls_ids.append(n_id)
        print(ls_ids)
        #logging.debug("1 record inserted, ID:", n_id)
        return n_id
    #this function needs to be tested:
    def append_df_rows(self, df_to_insert, s_table_name):
        df_to_insert.to_sql(name=s_table_name, con=self.m_oConn, if_exists = 'append', index=False, flavor = 'mysql')
    def commit(self):
        o_cursor = self.m_oConn.cursor()
        o_cursor.commit()
        #in the insert_row method the o_cursor.rowcount has the real number of rows inserted
        #here it always returns -1
        #print(o_cursor.rowcount, "record inserted.")
    def rollback(self):
        o_cursor = self.m_oConn.cursor()
        o_cursor.rollback()
# o_db_conn = CDbCon()
# o_db_conn.Connect()
# df = o_db_conn.ReadSqlQuery('select * from resident')
# print(df.head())
# print('done')