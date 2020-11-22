from flask import Flask, Response, render_template, jsonify
import json
import sqlite3

#地図作成用
import folium
from folium.plugins import HeatMap

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

#地図の生成
@app.route('/mapping', methods=["GET", "POST"])
def mapping():
    # 地図の中心を大手町にセット
    map = folium.Map(location=[35.6553, 139.7571], zoom_start=14)

    # プロットするデータのリスト
    list = []
    #con = sqlite3.connect(dbname)
    #cur = con.cursor()

    # 浜松町追加
    #result = cur.execute("SELECT COUNT(*) FROM homes WHERE erea_id == 新宿 and wake_up == 1")
    #sinzyuku = result.fetchone()
    #sinzyuku = sinzyuku[0]
    sinzyuku = 100
    for _ in range(sinzyuku):
        list.append([35.6553, 139.7571])

    # 赤羽追加
    #result = cur.execute("SELECT COUNT(*) FROM homes WHERE erea_id == 赤羽 and wake_up == 1")
    #akabane = result.fetchone()
    #akabane = akabane[0]
    akabane = 40
    for _ in range(akabane):
        list.append([35.777615, 139.7209868])  

    # 汐留追加
    # result = cur.execute("SELECT COUNT(*) FROM homes WHERE erea_id == 汐留 and wake_up == 1")
    # shiodome = result.fetchone()
    # shiodome = shiodome[0]
    shiodome = 35
    for _ in range(shiodome):
        list.append([35.6629339, 139.7600031])

    #cur.close() 
    #con.close()

    # データをヒートマップとしてプロット
    HeatMap(list, radius=40, blur=40).add_to(map)

    # HTMLを出力
    map.save('templates/tmpl.html')

    return render_template('tmpl.html')

app.run(debug=True)