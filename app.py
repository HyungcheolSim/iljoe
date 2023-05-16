from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.chtiogv.mongodb.net/?retryWrites=true&w=majority')
db = client.dbProject

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title':ogtitle,
        'desc':ogdesc,
        'image':ogimage,
        'comment':comment_receive
    }

    db.sparta2.insert_one(doc)


    return jsonify({'msg':'저장 완료!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    all_movies = list(db.sparta2.find({},{'_id':False}))
    return jsonify({'msg':'GET 연결 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
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



