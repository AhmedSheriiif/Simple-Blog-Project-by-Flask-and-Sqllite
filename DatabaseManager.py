import mysql.connector as mysql


class Database:
    # Connect to database
    def __init__(self, db_name):
        try:
            self.db = mysql.connect(
                host="localhost",
                user="root",
                password="",
                database=db_name
            )
            self.cursor = self.db.cursor()
            print("Connected to Database Successfully")
        except:
            print("Failed to connect to Database")

    # Check username and password
    def check_login(self, username, password):
        try:
            self.cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
            result = self.cursor.fetchone()
            if result:
                return True
            else:
                return False
        except:
            print("Failed to check login")

    # Check username exists
    def check_username(self, username):
        try:
            self.cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            result = self.cursor.fetchone()
            if result:
                return True
            else:
                return False
        except:
            print("Failed to check username")

    # Check email exists
    def check_email(self, email):
        try:
            self.cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            result = self.cursor.fetchone()
            if result:
                return True
            else:
                return False
        except:
            print("Failed to check email")

    # Register new user
    def register(self, username, password, email):
        try:
            self.cursor.execute("INSERT INTO user (username, password, email) VALUES (%s, %s, %s)",
                                (username, password, email))
            self.db.commit()
            print("User registered successfully")
        except:
            print("Failed to register user")

    # Get UserID from username
    def get_user_id(self, username):
        try:
            self.cursor.execute("SELECT id FROM user WHERE username = %s", (username,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except:
            print("Failed to get user id")

    # Get all articles for a user
    def get_user_articles(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM article WHERE user_id = %s", (user_id,))
            result = self.cursor.fetchall()
            return result

        except:
            print("Failed to get user articles")

    # Add article to database
    def add_article(self, title, content, user_id):
        try:
            self.cursor.execute("INSERT INTO article (title, description, user_id) VALUES (%s, %s, %s)",
                                (title, content, user_id))
            self.db.commit()
            print("Article added successfully")
        except:
            print("Failed to add article")

    # Update article in database
    def update_article(self, article_id, title, content):
        try:
            self.cursor.execute("UPDATE article SET title = %s, description = %s WHERE article_id = %s", (title, content, article_id))
            self.db.commit()
            print("Article updated successfully")
        except:
            print("Failed to update article")

    # Get article from database by id
    def get_article(self, article_id):
        try:
            self.cursor.execute("SELECT * FROM article WHERE article_id = %s", (article_id,))
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return None
        except:
            print("Failed to get article")

    # Delete article from database by id
    def delete_article(self, article_id):
        try:
            self.cursor.execute("DELETE FROM article WHERE article_id = %s", (article_id,))
            self.db.commit()
            print("Article deleted successfully")
        except:
            print("Failed to delete article")
