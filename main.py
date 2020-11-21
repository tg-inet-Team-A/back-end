from flask import Flask, Response
import json
import sqlite3

app = Flask(__name__)


# データベースファイルのパスを設定
dbname = 'database.db'

# テーブルの作成
con = sqlite3.connect(dbname)
cur = con.cursor()
create_table = 'create table if not exists ereas(id int, name text)'
create_table = 'create table if not exists house(id int, erea_id int, wake_up boolean)'
cur.execute(create_table)
con.commit()
cur.close() 
con.close()

@app.route('/erea/<erea_id>/wakeup_people', methods=["GET", "POST"])
def count(erea_id=None):
    return Response(response=json.dumps({'erea_id': erea_id, "wakeup_people": 0}), status=500)

app.run(debug=True)