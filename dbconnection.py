import psycopg2


"""
database management
"""


class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(dbname="electiontest",
                                    host="localhost",
                                    user = "postgres",
                                    password = "1234",
                                    port = "5432")
            self.cursor = self.conn.cursor()
            print("SUCCESFULLY CONNECTED TO DATABASE")
        except Exception as e:
            print("Error occured ", e)

    """
    query
    create table if not exists data(
    id SERIAL unique, --SERIAL only works for postgres
    name TEXT PRIMARY KEY,
    votes int default 0
);
"""

    def update_database(self, name):
        # gets the name of applicant to increase the vote of
        query = f"""update data set votes = votes + 1 where name = '{name}' ;"""
        self.cursor.execute(query)
        self.conn.commit()
        print("UPDATED FOR ",name)

    def ENDCONNECTION(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    Database()