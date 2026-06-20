import bcrypt
import jwt
import datetime
import os
from database.database import get_db

SECRET_KEY = os.getenv("SECRET_KEY", "diet_secret")

class AuthService:
    
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )
    
    @staticmethod
    def verify_password(password, hashed):
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed
        )
    
    @staticmethod
    def create_user(username, password):
        hashed = AuthService.hash_password(password)
        conn = get_db()
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def find_user(username):
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()
        return user
    
    @staticmethod
    def generate_token(user_id):
        token = jwt.encode({
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() +
                   datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")
        return token