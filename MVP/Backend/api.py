from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
from flask_cors import CORS

client = MongoClient("mongodb+srv://AdminUser:B3InTIN9rNbxb0EY@cluster0.abewe.mongodb.net/projectData?retryWrites=true&w=majority")
db = client.CPTS322GroupProject

app = Flask(__name__)
CORS(app)

@app.before_request
def interpretData():
    if request.data:
        request.data = json.loads(request.data)

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return jsonify({'name':'Jimit',
                    'address':'India'})

@app.route('/landscape/', methods=['POST'])
def add_landscape():
    data = request.data

    # make sure author exists
    print(data)
    status = db.landscapes.insert_one({
        "authorEmail" : data["authorEmail"],
        "title" : data["title"],
        "content": data["content"]
    })

    res = db.landscapes.find_one(status.inserted_id)
    res['id'] = str(res['_id'])
    del res['_id']

    print("-----------------------------------")
    print(json.dumps({
        'message' : 'SUCCESS',
        'data': res
    }))
    print("-----------------------------------")

    return json.dumps({
        'message' : 'SUCCESS',
        'data': res
    }), 200


@app.route('/landscape/', methods=['GET'])
def all_landscapes():
    landscapes, res = db.landscapes.find(), []

    for landscape in landscapes:
        landscape['id'] = str(landscape['_id'])
        del landscape['_id']
        res.append(landscape)

    return json.dumps({
        'message': 'SUCCESS',
        'data': res
    })


@app.route('/landscape/<string:id>', methods = ['GET'])
def select_landscape(id):
    target = db.landscapes.find_one({"_id": ObjectId(id)})
    target['id'] = str(target['_id'])
    del target['_id']

    return json.dumps({
        'message' : 'SUCCESS',
        'data': target
    }), 200

@app.route('/user/', methods=['POST'])
def add_user():
    data = request.data

    # make sure user doesn't already exist

    status = db.users.insert_one({
        "email": data["email"],
        "username": data["username"]
    })

    res = db.users.find_one(status.inserted_id)
    res['id'] = str(res['_id'])
    del res['_id']

    return json.dumps({
        'message' : 'SUCCESS',
        'data': res
    }), 200



@app.route('/comment/', methods=['POST'])
def add_comment():
    data = request.data 
    
    # make sure user exists
    # make sure landscape exists

    status = db.comments.insert_one({
        "authorEmail": data['authorEmail'],
        "landscape_id": data['landscape_id'],
        "content": data['content'],
        "likes": 0
    })

    res = db.comments.find_one(status.inserted_id)
    res['id'] = str(res['_id'])
    del res['_id']

    return json.dumps({
        'message' : 'SUCCESS',
        'data': res
    }), 200


@app.route('/comment/<string:ls_id>', methods=['GET'])
def get_comments(ls_id):
    comments, res = db.comments.find({"landscape_id": ls_id}), []
    for comment in comments:
        comment['id'] = str(comment['_id'])
        del comment['_id']
        res.append(comment)

    return json.dumps({
        'message': 'SUCCESS',
        'data': res
    })


@app.route('/comment/<string:c_id>', methods = ['PATCH'])
def patch_comment(c_id):
    c = db.comments.find_one(ObjectId(c_id))
    
    status = db.comments.update_one(c, {"$set": { "likes": c['likes'] + 1}})

    res = db.comments.find_one(c['_id'])
    res['id'] = str(res['_id'])
    del res['_id']

    return json.dumps({
        'message': 'SUCCESS',
        'data': res
    })


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
        

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True) 
