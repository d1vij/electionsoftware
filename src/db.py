import psycopg2


"""
database management
"""
"""
    create table query ->

    create table if not exists <postName>(
    name TEXT PRIMARY KEY,
    votes int default 0,
    check( votes >= 0)
);
"""

class Database:
    def __init__(self):
        self.cursor = None
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(dbname="electiontest",
                                    host="localhost",
                                    user = "postgres",
                                    password = "1234",
                                    port = "5432")

            self.cursor = self.conn.cursor()
            return "CONNECTION_SUCCESS"
        except Exception as e:
            return f"Error occurred : {e}"

    def increment_vote(self,table_name : str,candidate_name : str):
        """
        execution of increment vote method is as follows
        database.increment_vote(<post_name>, <value form the corresponding radio button>)
        e.g. database.increment_vote("somepost","divij")
        """
        if table_name=="NONE":return
        query = f"update {table_name} set votes = votes + 1 where name = '{candidate_name}' ;"
        self.cursor.execute(query)
        self.conn.commit()
        print(f"Incremented vote for candidate : {candidate_name} for the post {table_name}.\n")

    def ENDCONNECTION(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    Database()