import pymysql
from flask import Flask, request, render_template, redirect


db = pymysql.connect("arishkage.mysql.pythonanywhere-services.com", "arishkage", "15101989python", "arishkage$url")

#pone el cursor en la DB
cursor = db.cursor()

base_url = 'http://arishkage.pythonanywhere.com/'
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']

        sql = "INSERT INTO url(ID,URL) VALUES (ID, '{}')".format( url)
        cursor.execute(sql)
        db.commit()

        short_url = cursor.lastrowid
        return render_template('newindex.html', short_url=base_url + str(short_url))
    return render_template('newindex.html')

@app.route('/<short_url>')
def redirect_url(short_url):
    sql = "select url from url where id = {}".format(short_url)
    cursor.execute(sql)
    url = cursor.fetchone()[0]

    return redirect(url)


if __name__ == '__main__':
    app.run()
