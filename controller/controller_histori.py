def format_histori_data(data):
    for item in data:
        item["_id"] = str(item["_id"])
        item["tanggal"] = item["tanggal"].isoformat()
    return data

def get_histori(histori_collection, user_id):
    data = list(histori_collection.find({"user_id": user_id}))
    return format_histori_data(data)

def get_histori_stats(histori_collection, user_id):
    total = histori_collection.count_documents({"user_id": user_id})
    return {"user_id": user_id, "total_records": total}

def get_histori_filtered(histori_collection, user_id, filter_type):
    query = {"user_id": user_id}
    if filter_type == "recent":
        data = list(histori_collection.find(query).sort("tanggal", -1).limit(5))
    else:
        data = list(histori_collection.find(query))
    return format_histori_data(data)
