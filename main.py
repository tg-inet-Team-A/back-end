from flask import Flask, Response, render_template
import json
import sqlite3
from flask_cors import CORS

#地図作成用
import folium
from folium.plugins import HeatMap

app = Flask(__name__)
CORS(app)


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

    res = json.dumps(res)
    return Response(response=res, status=200)

#地図の生成
@app.route('/mapping', methods=["GET", "POST"])
def mapping():
    # 地図の中心を大手町にセット
    map = folium.Map(location=[35.684952, 139.769842], zoom_start=12)

    # プロットするデータのリスト
    list = [
    [35.68075751, 139.76717134],
    [35.68330693, 139.76900625],
    [35.66299721, 139.73246813]
    ]

    # 地図にプロット
    # con = sqlite3.connect(dbname)
    # cur = con.cursor()
    # table = cur.execute("SELECT id FROM ereas")

    # for i in table:
    #     if table[i] == "新宿":
    #        list.append([0000, 00000])
    # cur.close() 
    # con.close()


    # データをヒートマップとしてプロット
    HeatMap(list, radius=4, blur=3).add_to(map)

    # HTMLを出力
    map.save('templates/tmpl.html')

    return render_template('tmpl.html')

app.run(debug=True)