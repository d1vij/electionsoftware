# default blueprint
import psycopg2

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(dbname="electiontest",
                                    host="localhost",
                                    user = "postgres",
                                    password = "1234",
                                    port = "5432")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Error occured ", e)
        self.test()
    def test(self):
        # self.cursor.execute("insert into data values(1,'divij',0),(2,'shinchan',0)")
        self.cursor.execute("update data set votes = votes + 1 where name = 'divij'")
        self.conn.commit()
        self.cursor.execute("select * from data")
        data = self.cursor.fetchall()
        print(data)



    def ENDCONNECTION(self):
        self.cursor.close()
        self.conn.close()

d = Database()