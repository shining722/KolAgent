from flask import current_app, jsonify



def set_key_with_ttl(key, value, ttl):
    current_app.redis_client.set(key, value, ttl)
    return jsonify({"message": f"Key '{key}' set to '{value}' ttl is '{ttl}'"})

def set_key(key, value):
    current_app.redis_client.set(key, value)
    return jsonify({"message": f"Key '{key}' set to '{value}'"})


def get_key(key):
    value = current_app.redis_client.get(key)
    if value:
        return jsonify({"key": key, "value": value})
    else:
        return jsonify({"error": f"Key '{key}' not found"}), 404

def delete_key(key):
    if current_app.redis_client.delete(key):
        return jsonify({"message": f"Key '{key}' deleted"})
    else:
        return jsonify({"error": f"Key '{key}' not found"}), 404