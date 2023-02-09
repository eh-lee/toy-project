from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://jjdc0809:jjhappy0809@cluster0.rjxea19.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/dashboard", methods=["POST"])
def gym_post():
    type_receive = request.form['type_give']
    sets_receive = request.form['sets_give']
    reps_receive = request.form['reps_give']
    comments_receive = request.form['comments_give']
    heart_receive = request.form['heart_give']
    dashboard_list = list(db.dashboard.find({}, {'_id': False}))
    count = len(dashboard_list) + 1

    doc = {
        'type' : type_receive,
        'sets' : sets_receive,
        'reps' : reps_receive,
        'comments' : comments_receive,
        'hearts' : heart_receive,
        'num' : count,
        'done' : 0
    }
    if comments_receive == "" :
        return jsonify({'msg' : '1'})
    else:
        db.dashboard.insert_one(doc)
        return jsonify({'msg': '2' })

@app.route("/dashboard/delete",methods=["POST"])
def del_dash():
    num_recieve = request.form['num_give']
    db.dashboard.update_one({'num' : int(num_recieve)}, {'$set': {'done': 1}})
    return jsonify({'msg' : 'update complete'})

@app.route("/dashboard", methods=["GET"])
def gym_get():
    dashboard_list = list(db.dashboard.find({}, {'_id': False}))
    return jsonify({'dashboards': dashboard_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)