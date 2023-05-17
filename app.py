from flask import Flask, render_template, request, jsonify, redirect
import random

app = Flask(__name__)

from bson.objectid import ObjectId
import certifi
ca = certifi.where()

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.32ylit8.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta
# print(list(db.members.find({})))

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/api/member", methods=["POST"])
def member_post():
    name_receive = request.form['name_give']
    blog_receive = request.form['blog_give']
    mbti_receive = request.form['mbti_give']
    img_receive = request.form['img_give']
    desc_receive = request.form['desc_give']
    merit_receive = request.form['merit_give']

    doc = {
        'name':name_receive,
        'blog':blog_receive,
        'mbti':mbti_receive,
        'img':img_receive,
        'desc':desc_receive,
        'merit':merit_receive
    }
    db.members.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

@app.route("/api/member", methods=["GET"])
def member_get():
    all_members = list(db.members.find({}))
    for member in all_members:
        member['_id'] = str(member['_id'])
    return jsonify({'result':all_members})


#상세보기
@app.route("/api/member/<id>", methods=["GET"])
def one_find_member(id):
    find_member = db.members.find_one({"_id": ObjectId(id)})
    find_member['_id'] = str(find_member['_id'])
    find_id = db.members.find_one({'_id' : ObjectId(id)},{'id':True})
    return render_template('view.html', member=find_member, member_id=find_id)

#수정
@app.route("/api/member/update/<id>", methods=["GET"])
def update_get(id):
    find_member = db.members.find_one({"_id": ObjectId(id)})
    find_member['_id'] = str(find_member['_id'])
    find_id = db.members.find_one({'_id' : ObjectId(id)},{'id':True})
    return render_template('update.html', member=find_member, member_id=find_id)

@app.route("/api/member/update/<id>", methods=["POST"])
def update_post(id):
    name_receive = request.form['name_give']
    blog_receive = request.form['blog_give']
    mbti_receive = request.form['mbti_give']
    img_receive = request.form['img_give']
    desc_receive = request.form['desc_give']
    merit_receive = request.form['merit_give']

    find_member = db.members.find_one({"_id": ObjectId(id)})
    find_member['_id'] = str(find_member['_id'])

    db.members.update_one({'_id': ObjectId(id)},{'$set':{'name':name_receive}})
    db.members.update_one({'_id': ObjectId(id)},{'$set':{'blog':blog_receive}})
    db.members.update_one({'_id': ObjectId(id)},{'$set':{'mbti':mbti_receive}})
    db.members.update_one({'_id': ObjectId(id)},{'$set':{'img':img_receive}})
    db.members.update_one({'_id': ObjectId(id)},{'$set':{'desc':desc_receive}})
    db.members.update_one({'_id': ObjectId(id)},{'$set':{'merit':merit_receive}})

    return redirect('/api/member/'+id)

#삭제
@app.route('/api/member/<id>', methods=['DELETE'])
def delete_post(id):
    del_member = db.members.find_one_and_delete({"_id": ObjectId(id)})

    if del_member:
        return jsonify({'msg':'삭제가 완료되었습니다..'})
    else:
        return jsonify({'msg':'팀원 조회가 되지 않습니다.'})


@app.route('/api/reply/', methods=['POST'])# 댓글입력
def input_comment():
    comment_receive = request.form['comment']
    id_receive = request.form['id']
    comment_id=id_receive+str(random.random())
    db.members.update_one({'_id':ObjectId(id_receive)}, {"$push":{"comments":[comment_receive,comment_id]}})
    return jsonify({'msg':'저장완료!'})

@app.route('/api/reply/<id>', methods=['GET']) # 댓글 출력
def show_comment(id):
    find_member = db.members.find_one({"_id": ObjectId(id)})
    find_member['_id'] = str(find_member['_id'])
    return jsonify({'result':find_member})

@app.route('/api/reply/del/<id>', methods=['POST']) # 댓글삭제
def del_comment(id):
    comment_id = request.form['comment_id']
    db.members.update_one({'_id':ObjectId(id)},{"$pull":{"comments": { "$elemMatch": { "$in": [comment_id] }}}})
    return jsonify({'msg':comment_id})

@app.route('/api/reply/update/<id>', methods=['POST']) # 댓글수정
def update_comment(id):
    fix_comment = request.form['fix_comment']
    comment_id = request.form['comment_id']
    len_comment = request.form['len_comment']
    for i in range(int(len_comment)):
        a=list(db.members.find({f"comments.{i}.1":  comment_id}))
        if len(a) !=0:
            db.members.update_one({f"comments.{i}.1":comment_id},{"$set":{f"comments.{i}.0": fix_comment}})
    return jsonify({'msg':'comment_id'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
