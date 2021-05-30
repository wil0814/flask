from flask import Flask, render_template, redirect, url_for, request, flash,jsonify
import pymysql,json
app = Flask(__name__)


#連線mysql
#conn = pymysql.connect(
#    host='localhost',
#    user='root',
#    password='',
#    db='test',
#    charset='utf8'
#)

@app.route('/addshopping', methods=['GET','POST'])
def addshopping():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    if  request.method == "POST":
        data = json.loads(request.get_data())
        did=data["name"]
        need=data["need"]
        cur=conn.cursor()
        sql="update shopping set need='"+need+"' where id='"+did+"';"
        cur.execute(sql)
        cur.close()
        conn.commit()
 


        return jsonify(data)
    else:
        return redirect(url_for('shopping'))










@app.route('/buy_all', methods=['GET','POST'])
def login():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )

    if  request.method == "POST": 
        data = json.loads(request.get_data())
        a=len(data["name"])

        for i in range(a):
            need=data["need"][i]
            did=data["name"][i]
            cur=conn.cursor()
            sql="update books set have=have-'"+need+"' where id='"+did+"';"
            cur.execute(sql)
            cur.close()
            conn.commit()

            cur=conn.cursor()
            sql="INSERT INTO sell (id,sell) values('"+did+"','"+need+"');"
            try:
                cur.execute(sql)
                cur.close()
                conn.commit()
            except:
                cur.close()
                conn.rollback()
                
            cur=conn.cursor()
            sql="update sell set sell=sell+'"+need+"' where id='"+did+"';"
            cur.execute(sql)
            cur.close()
            conn.commit()

            cur=conn.cursor()
            sql="delete from shopping where id='"+did+"';"
            cur.execute(sql)
            cur.close()
            conn.commit()
        return jsonify(data) 
    else: 
        return redirect(url_for('shopping')) 






@app.route('/buy')
def index():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books"
    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    return render_template('buy.html',content=content)

@app.route('/chinese')
def chinese():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where class='中文書'"
    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    return render_template('chinesebook.html',content=content)

@app.route('/english')
def english():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where class='英文書'"
    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    return render_template('english.html',content=content)


@app.route('/sellgood')
def sellgood():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select sell.id, sell.sell, books.bookname, books.photo, books.money, books.出版日期 from sell inner join books on sell.id=books.id order by sell desc;"
    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    return render_template('/sellgood.html',content=content)






@app.route('/shopping', methods=['GET','POST'])
def shopping():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    if request.method == 'POST':
        num=request.values['num']
        need=request.values['need']
        cur=conn.cursor()
        sql="INSERT INTO shopping (id,need) values('"+num+"','"+need+"');"
        try:
            cur.execute(sql)
            cur.close()
            conn.commit()
        except:
            cur.close()
            conn.rollback()
        

        cur=conn.cursor()
        #sql="select * from shopping;"
        #cur.execute(sql)
        #content = cur.fetchall()
       # payload=[]                     迴圈跑mysql變成json格式
       # contentJ={}
       # for result in content:
       #     contentJ={'id':result[0]}
       #     payload.append(contentJ)
       #     contentJ={}

        sql="select shopping.id, shopping.need, books.photo, books.money, books.bookname  from shopping inner join books on shopping.id=books.id;"
        cur.execute(sql)
        content = cur.fetchall()
        data = list(map(list,content))
        cur.close()
        datalong=len(data)
        #return render_template('/hello.html')
        return render_template('/shopping.html',content=data,longdata=datalong)
    



    cur=conn.cursor()
    sql="select shopping.id, shopping.need, books.photo, books.money, books.bookname  from shopping inner join books on shopping.id=books.id;"
    cur.execute(sql)
    content = cur.fetchall()
    data = list(map(list,content))
    cur.close()
    datalong=len(data)
    return render_template('/shopping.html',content=content,longdata=datalong)

    



@app.route('/shopping/delete', methods=['GET','POST'])
def delete():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    if request.method == 'POST':
        did=request.values['did']
        cur=conn.cursor()
        sql="delete from shopping where id='"+did+"';"
        cur.execute(sql)
        cur.close()
        conn.commit()
        return redirect(url_for('shopping'))
    return redirect(url_for('shopping'))


@app.route('/shopping/buy', methods=['GET','POST'])
def buy():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    if request.method == 'POST':
        did=request.values['did']
        need=request.values['need']
        intneed=int(need)
        cur=conn.cursor()
        sql = "select have from books where id ='"+did+"';"
        cur.execute(sql)
        content = cur.fetchone()
        cur.close()
        if  intneed < content[0]:
            
            cur=conn.cursor()
            sql="INSERT INTO sell (id,sell) values('"+did+"','"+need+"');"
            try:
                cur.execute(sql)
                cur.close()
                conn.commit()
            except:
                cur.close()
                conn.rollback()


            cur=conn.cursor()
            sql="update sell set sell=sell+'"+need+"' where id='"+did+"';"
            cur.execute(sql)
            cur.close()
            conn.commit()

            cur=conn.cursor()
            sql="update books set have=have-'"+need+"' where id='"+did+"';"
            cur.execute(sql)
            cur.close()
            conn.commit()
            cur=conn.cursor()
            sql="select * from books where id ='"+did+"';"
            cur.execute(sql)
            content = cur.fetchall()
            cur.close()
            cur=conn.cursor()
            sql="delete from shopping where id='"+did+"';"
            cur.execute(sql)
            cur.close()
            conn.commit()
            flash('購買成功')
            return redirect(url_for('shopping'))
            
        else:
            flash('庫純不足')
            return redirect(url_for('shopping'))
    
    return redirect(url_for('shopping'))





@app.route('/buy/0001', methods=['GET','POST'])
def b0001():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='女性貧困: 負貸、漂流、未婚單親, 陷入惡性循環的貧困女子'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)

@app.route('/buy/0002')
def b0002():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='海洋解剖書: 超過650幅海洋博物繪, 帶你深入淺出, 全方位探索洋流、地形、鯨豚等自然知識'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)
@app.route('/buy/0003')
def b0003():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='你並非一無所有: 你還有病及未拆的快遞和未完成的夢想 (翔翔獨家限量贈送-毒家小天後語錄小本本)'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)
@app.route('/buy/0004')
def b0004():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='茶風味學: 焙茶師拆解茶香口感的秘密, 深究產地、製茶工序與焙火變化創作'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)

@app.route('/buy/00015')
def b0005():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='光天化日搶錢: 稅賦如何形塑過去與改變未來?'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)

@app.route('/buy/0006')
def b0006():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='我是遺物整理師'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)


@app.route('/buy/0007')
def b0007():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='金融怪傑．達文熙教你用100張圖學會箱子戰法: 傳承60年經典理論, 融合台股贏家思維'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)


@app.route('/buy/0008')
def b0008():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='流動的疆域: 全球視野下的雲南與中國'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)

@app.route('/buy/0009')
def b0009():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='流動瑜伽的身心回正練習: 人氣YT頻道凱蒂瑜伽全新編排!'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)

@app.route('/buy/00010')
def b00010():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='生氣得剛剛好: 與憤怒共處的正念練習'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)

@app.route('/buy/00011')
def b00011():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='愛我, 殺了我 (誠品獨家賽璐珞書衣版)'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)


@app.route('/buy/00014')
def b00012():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='武漢封城日記'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)

@app.route('/buy/00016')
def b00016():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
    cur=conn.cursor()
    sql = "select * from books where bookname ='The Death of Francis Bacon'"
    cur.execute(sql)
    content = cur.fetchall()
    return render_template('/book/0001.html',content=content)



@app.route('/mysqltest', methods=['GET','POST'])
def mysqltest():
    if request.method == 'POST':
        conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='subject',
        charset='utf8'
        )
        cur=conn.cursor()
        class1=request.values['class']
        photo=request.values['photo']
        recommend=request.values['recommend']
        bookname=request.values['bookname']
        littleword=request.values['littleword']
        author=request.values['author']
        publishing=request.values['publishing']
        date=request.values['date']
        money=request.values['money']
        have=request.values['have']

        sql="INSERT INTO books (class,photo,recommend,bookname,littleword,Author,Publishing,出版日期,money,have) values('"+class1+"','"+photo+"','"+recommend+"','"+bookname+"','"+littleword+"','"+author+"','"+publishing+"','"+date+"','"+money+"','"+have+"');"
        #sql="INSERT INTO newbook (photo,recommend) VALUES ('"+photo+"','"+recommend+"');"
        cur.execute(sql)
        conn.commit()
        return 'hello'+bookname
    return render_template('/mysqlinput.html')




    



















if __name__ == '__main__':
    app.debug = True
    app.secret_key = "Your Key"
    app.run()

















