import pymysql
from flask import Flask, request, render_template, redirect
import hashlib

db = pymysql.connect(host_url, username, password, database)
cursor = db.cursor() 
base_url = 'http://tbvescio.pythonanywhere.com/'
app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home():
    db = pymysql.connect(host_url, username, password, database)
    cursor = db.cursor()
    if request.method == 'POST':

        url = request.form['url'] 

        hash_url = hashlib.sha1(url.encode("UTF-8")).hexdigest() #convierte url a hash
        hash_url = hash_url[:7] 

        sql = "INSERT INTO url(ID,URL,HASH) VALUES (ID, '{}','{}')".format(url,hash_url)
        cursor.execute(sql)
        db.commit()
        cursor.close()


        return render_template('url.html', short_url=base_url + str(hash_url))
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_url(short_url):
    db = pymysql.connect(host_url, username, password, database)
    cursor = db.cursor()

    sql = "select url from url where HASH = '{}'".format(short_url)
    cursor.execute(sql)
    url = cursor.fetchone()[0] 
    cursor.close()
    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True)
