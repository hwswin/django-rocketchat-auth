import hashlib
import random
import string
from pymongo import MongoClient
from django.conf import settings

def generate_token(n=50):
    chars = string.ascii_letters + string.digits
    token = ''.join(random.SystemRandom().choice(chars) for _ in range(n))
    token = hashlib.sha1(token.encode()).hexdigest()

    return token


def create_user(email, fullname, username):
    client = MongoClient("mongodb://" + settings.MONGO_DB)
    mongo = client.rocketchat

    user = mongo.users.find_one({'username': username})
    if not user:

        headers = {
            'X-Auth-Token': ROCKETCHAT_AUTH_TOKEN,
            'X-User-Id': ROCKETCHAT_USER_ID,
        }
        data = {
            'email': email,
            'name': name,
            'username': username,
            'password': helpers.generate_token(),
        }
        requests.get(settings.ROCKETCHAT_URL + '/api/v1/users.create',
                     headers=headers, data=data)

        user = mongo.users.find_one({'username': username})

    user['services'] = {'iframe': {'token': helpers.generate_token()}}
    mongo.users.update_one({'_id': user['_id']}, {'$set': user})

    return user['services']['iframe']['token']
