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
def member_post():
    name_receive = request.form['name_give']
    blog_receive = request.form['blog_give']
    mbti_receive = request.form['mbti_give']

    doc = {
        'name':name_receive,
        'blog':blog_receive,
        'mbti':mbti_receive
    }
    db.members.insert_one(doc)
    print(name_receive, blog_receive, mbti_receive)


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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)



