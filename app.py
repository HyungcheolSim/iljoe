from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from bson.objectid import ObjectId

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.32ylit8.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/member", methods=["POST"])
def main_post():
    mbti_receive = request.form['mbti_give']
    merit_receive = request.form['merit_give']
    blog_receive = request.form['blog_give']
    desc_receive = request.form['desc_give']

    doc = {
        'blog':blog_receive,
        'mbti':mbti_receive,
        'merit':merit_receive,
        'desc':desc_receive
    }

    db.main.insert_one(doc)
    print(blog_receive, mbti_receive, merit_receive, desc_receive)

@app.route("/api/member", methods=["POST"])
def member_post():
    index_receive = request.form['index_give']
    name_receive = request.form['name_give']
    profile_receive = request.form['profile_give']

    doc = {
        'index':index_receive,
        'name':name_receive,
        'profile':profile_receive
    }

    db.members.insert_one(doc)
    print(index_receive, name_receive, profile_receive)

    return jsonify({'msg':'저장완료!'})

@app.route("/member", methods=["GET"])
def member_get():
    all_members = list(db.members.find({}))
    for member in all_members:
        member['_id'] = str(member['_id'])
    return jsonify({'result':all_members})

@app.route("/view/<id>", methods=["GET"])
def one_find_member(id):
    find_member = db.members.find_one({"_id": ObjectId(id)})
    find_member['_id'] = str(find_member['_id'])
    find_id = db.members.find_one({'_id' : ObjectId(id)},{'id':True})
    return render_template('view.html', member=find_member, member_id=find_id)

@app.route("/api/member", methods=["GET"])
def main_get():
    all_lists = list(db.main.find({},{'_id':False}))
    return jsonify({'msg':'전송완료'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)



