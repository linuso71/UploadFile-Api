# pip install mysql-connector-python==8.0.23
import mysql.connector
from mysql.connector import Error

# connect to the database server
class DB:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host='127.0.0.1',
                user = 'root',
                password = 'linus',
                database = 'interview'
            )
            self.mycursor = self.conn.cursor()
            print('connection established')
        except:
            print('connection error')

    def register(self,name,email,password):
        self.mycursor.execute("""
        INSERT INTO users (email,username,password)
        VALUES ('{}','{}','{}')
        """.format(email,name,password))
        self.conn.commit()
        return True

    def search(self,email,password):
        self.mycursor.execute("""
        SELECT email FROM users
        where email = '{}' and password = '{}'
        """.format(email,password))
        try:
            self.mycursor.fetchall()[0][0]
            return True
        except:
            return False

    def upload_file(self,filename):
        # self.mycursor.execute('INSERT INTO uploads (id,filename) VALUES (?)', (1,filename,))
        # self.conn.commit()
        try:
            if self.conn.is_connected():
                self.mycursor.execute('INSERT INTO files (filename) VALUES (%s)', (filename,))
                self.conn.commit()

        except Error as e:
            print(f"Error: {e}")
        # finally:
        #     if self.conn.is_connected():
        #         self.mycursor.close()
        #         self.conn.close()

    def delete_file(self,filename):
        self.mycursor.execute("DELETE FROM interview.files WHERE filename = '{}' ".format(filename))
        self.conn.commit()

    def search_file(self,id):
        self.mycursor.execute("SELECT filename FROM interview.files where id = '{}'".format(id))
        result = self.mycursor.fetchall()
        if result:
            return result[0][0]
        else:
            print('not found')

    def update_file(self,id,filename):
        self.mycursor.execute("UPDATE interview.files SET filename = '{}' WHERE id = '{}'".format(filename,id))
        self.conn.commit()






## create database
# mycursor.execute("create database interview")
# conn.commit()

# creating user table
# obj = DB()
# obj.search_file(1)

# obj.mycursor.execute("""
#     CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     email VARCHAR(255) NOT NULL,
#     username VARCHAR(255) NOT NULL,
#     password VARCHAR(255) NOT NULL
# )
# """)
# obj.conn.commit()

# creating file table

# mycursor.execute("""
# CREATE TABLE files (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     filename VARCHAR(255) NOT NULL,
#     path VARCHAR(255) NOT NULL
# )
# """)
# conn.commit()