from flask import Flask, render_template, request, jsonify
import random
app = Flask(__name__)

from bson.objectid import ObjectId
import certifi
from pymongo import MongoClient
ca = certifi.where()

client = MongoClient('mongodb+srv://Jacksoon:test@cluster1.bv8ib2u.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.temp

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/member", methods=["GET"])
def member_get():
    all_members = list(db.users.find({}))
    all_members[0]['_id'] = str(all_members[0]['_id'])
    return jsonify({'result':all_members[0]})

@app.route("/member/comment", methods=["POST"])
def comment_seve():
    comment_receive = request.form['comment']
    id_receive = request.form['id']
    comment_id=id_receive+str(random.random())
    db.users.update_one({'_id':ObjectId(id_receive)}, {"$push":{"comments":[comment_receive,comment_id]}})
    return jsonify({'msg':id_receive})

@app.route("/member/comment/delete", methods=["POST"])
def comment_delete():
    comment_id = request.form['comment_id']
    id_receive = request.form['id']

    # db.users.update_one({} ,{ "$pull": { "comments": { "$elemMatch": {'1': comment_id}}}})
    db.users.update_one({'_id':ObjectId(id_receive)},{"$pull":{"comments": { "$elemMatch": { "$in": [comment_id] }}}})
    return jsonify({'msg':comment_id})
@app.route("/member/comment/fix", methods=["POST"])
def comment_fix():
    fix_comment = request.form['fix_comment']
    comment_id = request.form['comment_id']
    len_comment = request.form['len_comment']
    # a = list(db.users.find({'comments':{"$elemMatch": {"comments.$.1": 'comment_id'}}},{'comments'}))
    for i in range(int(len_comment)):
        a=list(db.users.find({f"comments.{i}.1":  comment_id}))
        if len(a) !=0:
            db.users.update_one({f"comments.{i}.1":comment_id},{"$set":{f"comments.{i}.0": fix_comment}})
    # db.users.update_one({'comments':{ "$elemMatch": { "$in": [comment_id]}}},{"$set":{"comments": {"$elemMatch": {'comments.$.0': fix_comment}}}})
    return jsonify({'msg':comment_id})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


