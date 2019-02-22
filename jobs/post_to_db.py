
class poster:
    def __init__(self, host, database, user, p, db_column_names):
        self.host = host
        self.database = database
        self.user = user
        self.himitsu = p
        self.cursor = None
        self.connection = None

    def get_connection(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                database=self.database,
                                user=self.user,
                                password=self.himitsu)
            if self.connection.is_connected():
                self.cursor = connection.cursor(buffered=True)

    def check_for_table(table_name, column_names):
        #create function to check for existence of table and create it if it doesn't exist
        pass

    def post_to_db(self, html_results_dict, table_name):
        column_name_tuple = ()
        sql_value_tuple = ()
        for label, value in html_results_dict:
            column_name_tuple = column_name_tuple + (lable,)
            sql_value_tuple = sql_value_tuple + (value,)
        sql_q_columns = str(column_name_tuple)
        sql_insert_query = """ INSERT INTO """+table_name+' '+sql_q_columns+ """ VALUES (%s,%s,%s)"""
        result  = cursor.execute(sql_insert_query, sql_value_tuple)
        connection.commit()
        print ("Record inserted successfully into python_users table")
        except mysql.connector.Error as error :
            connection.rollback()
            print("Failed to insert into MySQL table {}".format(error))

    def close_it_down(self):
        self.cursor.close()
        self.connection.close()
        print("MySQL connection is closed")