from models.model_terapi import TerapiModel

model = None

def set_db(db):
    global model
    model = TerapiModel(db)

def get_all_terapi():
    return model.get_all_terapi()

def get_terapi_by_id(terapi_id):
    return model.get_terapi_by_id(terapi_id)

def add_terapi(data):
    return model.add_terapi(data)

def update_terapi(terapi_id, data):
    model.update_terapi(terapi_id, data)

def delete_terapi(terapi_id):
    model.delete_terapi(terapi_id)
