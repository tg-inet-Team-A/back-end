from flask import Flask, Response, render_template, jsonify
import json
import sqlite3
from flask_cors import CORS

#地図作成用
import folium
from folium.plugins import HeatMap

app = Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False

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
id_num = [i for i in range(3)]
erea_name = ["浜松", "赤羽", "汐留"]
con = sqlite3.connect(dbname)
cur = con.cursor()
# insert = 'insert into homes(id, erea_id, wake_up) values (?,?,?)'
# home_id = [i for i in range(200)]
# erea_id = [2 for i in range(200)]
# wake_up = [0 for i in range(168)] + [1 for i in range(32)]
# for i in range(len(home_id)):
#     cur.execute(insert, (home_id[i], erea_id[i], wake_up[i]))

insert = 'insert into ereas(id, name) values (?,?)'
for i in range(len(id_num)):
    cur.execute(insert, (id_num[i], erea_name[i]))

con.commit()
cur.close() 
con.close()

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
    return Response(response=json.dumps({'erea_id': erea_id, "wakeup_people": num}), status=200)


@app.route('/erea/all', methods=["GET", "POST"])
def erea_name():
    con = sqlite3.connect(dbname)
    cur = con.cursor()

    # カウント処理
    sql = "SELECT * FROM ereas"
    result = cur.execute(sql)
    
    res = []
    for column in result:
        res.append({'erea_id':column[0], 'erea_name':column[1]})

    cur.close() 
    con.close()

    res = json.dumps(res, ensure_ascii=False)
    return Response(response=res, status=200)

#地図の生成
@app.route('/mapping', methods=["GET", "POST"])
def mapping():
    # 地図の中心を大手町にセット
    map = folium.Map(location=[35.6553, 139.7571], zoom_start=14)

    # プロットするデータのリスト
    list = []
    
    # 浜松町追加
    hamamatsu = 100
    for _ in range(hamamatsu):
        list.append([35.6553, 139.7571])

    # 赤羽追加
    akabane = 40
    for _ in range(akabane):
        list.append([35.777615, 139.7209868])  

    # 汐留追加
    shiodome = 35
    for _ in range(shiodome):
        list.append([35.6629339, 139.7600031])

    # データをヒートマップとしてプロット
    HeatMap(list, radius=40, blur=40).add_to(map)

    # HTMLを出力
    map.save('templates/tmpl.html')

    return render_template('tmpl.html')

app.run(debug=True)