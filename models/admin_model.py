class Admin:
    _db = None
    _collection_name = 'admins'  # Sesuaikan nama koleksi di MongoDB

    @classmethod
    def set_db(cls, db):
        cls._db = db

    @classmethod
    def find_by_username(cls, username):
        if cls._db is None:
            raise Exception("Database belum di-set di model Admin")
        return cls._db[cls._collection_name].find_one({"username": username})

    @classmethod
    def insert_admin(cls, username, password):
        if cls._db is None:
            raise Exception("Database belum di-set di model Admin")
        # Simpan password dengan hash misalnya
        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)
        admin_data = {
            "username": username,
            "password": hashed_password
        }
        return cls._db[cls._collection_name].insert_one(admin_data)

    @classmethod
    def verify_password(cls, username, password):
        if cls._db is None:
            raise Exception("Database belum di-set di model Admin")
        from werkzeug.security import check_password_hash
        admin = cls.find_by_username(username)
        if admin and check_password_hash(admin['password'], password):
            return admin
        return None

    @classmethod
    def update_admin(cls, admin_data):
        """
        admin_data: dict minimal harus ada key 'username' dan field lain yang mau diupdate.
        Contoh: {'username': 'admin@example.com', 'email': 'baru@example.com', 'name': 'Nama Baru'}
        """
        if cls._db is None:
            raise Exception("Database belum di-set di model Admin")
        username = admin_data.get('username')
        if not username:
            raise ValueError("Username harus disertakan untuk update")

        # Buat dict update dengan menghapus username karena tidak diupdate
        update_fields = admin_data.copy()
        update_fields.pop('username', None)

        if not update_fields:
            raise ValueError("Tidak ada field yang diupdate")

        result = cls._db[cls._collection_name].update_one(
            {"username": username},
            {"$set": update_fields}
        )
        return result.modified_count > 0
