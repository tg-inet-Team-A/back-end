from flask import Flask, Response
import json
import sqlite3

app = Flask(__name__)


# データベースファイルのパスを設定
dbname = 'database.db'

# テーブルの作成
con = sqlite3.connect(dbname)
cur = con.cursor()
create_table1 = 'create table if not exists homes(id int, erea_id int, wake_up boolean)'
create_table2 = 'create table if not exists ereas(id int, name text)'
cur.execute(create_table1)
cur.execute(create_table2)
con.commit()
cur.close() 
con.close()

@app.route('/erea/<erea_id>/wakeup_people', methods=["GET", "POST"])
def count(erea_id=None, home_id =None):
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    table = cur.execute("SELECT * FROM ereas WHERE id == erea_id")
    num = 0
    for i in table:
        num += 1

    table = cur.execute("UPDATE homes SET wake_up =1 WHERE id = home_id")
    cur.close() 
    con.close()
    return Response(response=json.dumps({'erea_id': erea_id, "wakeup_people": num}), status=500)

app.run(debug=True)