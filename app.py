# from crypt import methods
import sqlite3
from flask import Flask, render_template
import json

var1='';

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('magnusa.db')#
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/ProcessUserinfo/<string:x>',methods=['POST'])

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM Fastag',(var1,)).fetchall()
    
    conn.close()
    return render_template('index.html', Fastag=posts)
    



def processFunc(x):
    x=json.loads(x)
    xi=x;
    print(xi);
    var1=xi;
    #return('/')

  