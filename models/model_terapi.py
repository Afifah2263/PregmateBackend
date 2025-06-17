from bson.objectid import ObjectId

class TerapiModel:
    def __init__(self, db):
        self.collection = db['terapi']

    def get_all_terapi(self):
        terapi_list = []
        for terapi in self.collection.find():
            terapi_list.append({
                '_id': str(terapi['_id']),
                'nama': terapi.get('nama', ''),
                'deskripsi': terapi.get('deskripsi', ''),
                'video_url': terapi.get('video_url', ''),
                'model_id': str(terapi.get('model_id', '')) if isinstance(terapi.get('model_id', ''), ObjectId) else terapi.get('model_id', ''),
                'landmark_referensi_id': str(terapi.get('landmark_referensi_id', '')) if isinstance(terapi.get('landmark_referensi_id', ''), ObjectId) else terapi.get('landmark_referensi_id', ''),
                'gambar': terapi.get('gambar', ''),
                'peringatan': terapi.get('peringatan', '')  # Menambahkan peringatan
            })
        return terapi_list

    def get_terapi_by_id(self, terapi_id):
        terapi = self.collection.find_one({'_id': ObjectId(terapi_id)})
        if terapi:
            return {
                '_id': str(terapi['_id']),
                'nama': terapi.get('nama', ''),
                'deskripsi': terapi.get('deskripsi', ''),
                'video_url': terapi.get('video_url', ''),
                'model_id': str(terapi.get('model_id', '')),
                'landmark_referensi_id': str(terapi.get('landmark_referensi_id', '')),
                'gambar': terapi.get('gambar', ''),
                'peringatan': terapi.get('peringatan', '')  # Menambahkan peringatan
            }
        return None

    def add_terapi(self, data):
        terapi = {
            'nama': data['nama'],
            'deskripsi': data['deskripsi'],
            'video_url': data['video_url'],
            'model_id': data['model_id'],
            'landmark_referensi_id': data['landmark_referensi_id'],
            'gambar': data['gambar'],
            'peringatan': data['peringatan'],  # Menambahkan peringatan
        }
        result = self.collection.insert_one(terapi)
        return str(result.inserted_id)

    def update_terapi(self, terapi_id, data):
        self.collection.update_one(
            {'_id': ObjectId(terapi_id)},
            {'$set': {
                'nama': data['nama'],
                'deskripsi': data['deskripsi'],
                'video_url': data['video_url'],
                'model_id': data['model_id'],
                'landmark_referensi_id': data['landmark_referensi_id'],
                'gambar': data['gambar'],
                'peringatan': data['peringatan'],  # Menambahkan peringatan
            }}
        )

    def delete_terapi(self, terapi_id):
        self.collection.delete_one({'_id': ObjectId(terapi_id)})
