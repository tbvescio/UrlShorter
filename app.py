import pymysql
from flask import Flask, request, render_template, redirect
import hashlib

db = pymysql.connect("tbvescio.mysql.pythonanywhere-services.com", "tbvescio", "15101989python", "tbvescio$url")
#db = pymysql.connect("localhost", "root", "15101989", "url")

cursor = db.cursor() #pone el cursor en la DB

base_url = 'http://tbvescio.pythonanywhere.com/'

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        db = pymysql.connect("localhost", "root", "15101989", "url")
        url = request.form['url'] #recive la url

        hash_url = hashlib.sha1(url.encode("UTF-8")).hexdigest() #convierte url a hash
        hash_url = hash_url[:7] #usa solo 7 chr del hash

        sql = "INSERT INTO url(ID,URL,HASH) VALUES (ID, '{}','{}')".format(url,hash_url)
        cursor.execute(sql)
        db.commit()


        return render_template('url.html', short_url=base_url + str(hash_url))
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_url(short_url):

    sql = "select url from url where HASH = '{}'".format(short_url)
    cursor.execute(sql)
    url = cursor.fetchone()[0] #guarda el resultado
    
    

if __name__ == '__main__':
    app.run(debug=True)
