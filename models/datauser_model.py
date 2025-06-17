from bson import ObjectId  # Impor ObjectId
import datetime

class User:
    # Menyimpan database MongoDB
    db = None

    @classmethod
    def set_db(cls, db):
        """Mengatur koneksi database."""
        cls.db = db
    @staticmethod
    def update_profile_picture(user_id, filename):
        try:
            users_collection = User.db['users']  # pastikan pakai User.db
            result = users_collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {'foto': filename}}
            )
            if result.modified_count == 1:
                return users_collection.find_one({'_id': ObjectId(user_id)})
            else:
                return None
        except Exception as e:
            print(f"Error updating profile picture: {e}")
            return None
    

    @staticmethod
    def find_by_id(user_id):
        """Mencari pengguna berdasarkan ID."""
        if User.db is None:
            raise Exception("Database connection is not initialized.")
        return User.db["users"].find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def find_all():
        """Mengambil semua pengguna."""
        if User.db is None:
            raise Exception("Database connection is not initialized.")
        return list(User.db["users"].find())

    @staticmethod
    def insert_user(user_data):
        """Menambahkan pengguna baru ke database."""
        if User.db is None:
            raise Exception("Database connection is not initialized.")
        result = User.db["users"].insert_one(user_data)
        return result.inserted_id

    @staticmethod
    def update(user_id, nama, email, password, foto=None):
        """Memperbarui data pengguna."""
        if User.db is None:
            raise Exception("Database connection is not initialized.")
        
        update_data = {
            "nama": nama,
            "email": email,
            "password": password,
        }

        if foto is not None:
            update_data["foto"] = foto

        result = User.db["users"].update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        if result.modified_count:
            return User.find_by_id(user_id)
        else:
            return None
    @staticmethod
    def update_fields(user_id, update_fields: dict):
        User.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
        return User.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def delete_user(user_id):
        """Menghapus pengguna berdasarkan user_id."""
        try:
            result = User.db["users"].delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    # pastikan di models/datauser_model.py sudah ada method find_by_email seperti ini:

    @staticmethod
    def find_by_email(email):
        """Mencari pengguna berdasarkan email."""
        if User.db is None:
            raise Exception("Database connection is not initialized.")
        return User.db["users"].find_one({"email": email})
  

    @classmethod
    def update_token(cls, user_id, token):
        return cls.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'tokenFCM': token}})


