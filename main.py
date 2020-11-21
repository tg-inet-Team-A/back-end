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

# 仮データの追加処理
# con = sqlite3.connect(dbname)
# cur = con.cursor()
# insert = 'insert into homes(id, erea_id, wake_up) values (?,?,?)'
# cur.execute(insert, (0, 0, 0))
# cur.execute(insert, (1, 0, 1))
# cur.execute(insert, (2, 0, 1))
# cur.execute(insert, (3, 1, 0))
# cur.execute(insert, (4, 1, 0))

# insert = 'insert into ereas(id, name) values (?,?)'
# cur.execute(insert, (0, "TOKYO"))
# cur.execute(insert, (1, "Osaka"))

# con.commit()
# cur.close() 
# con.close()

@app.route('/erea/<erea_id>/wakeup_people', methods=["GET", "POST"])
def count(erea_id=None, home_id =0):
    erea_id = int(erea_id)
    con = sqlite3.connect(dbname)
    cur = con.cursor()

    # カウント処理
    sql = "SELECT COUNT(*) FROM homes WHERE erea_id == ? and wake_up == 1"
    result = cur.execute(sql, (erea_id, ))
    num = result.fetchone()
    num = num[0]
    
    # 起床処理
    sql = "UPDATE homes SET wake_up =1 WHERE id = ?"
    cur.execute(sql, (home_id, ))
    con.commit()

    cur.close() 
    con.close()
    return Response(response=json.dumps({'erea_id': erea_id, "wakeup_people": num}), status=500)

app.run(debug=True)