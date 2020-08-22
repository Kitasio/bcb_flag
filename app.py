import os
import sqlite3
from flask import Flask, render_template, url_for
from flask import request

def number_cleaner(item):
    number = ''.join(filter(str.isdigit, str(item)))
    return int(number)

def ip_counter(client_ip=1):
    conn = sqlite3.connect('ip_database.db')
    c = conn.cursor()
    cleaned_ip = number_cleaner(client_ip)

    # Creates table
    c.execute("CREATE TABLE IF NOT EXISTS ips (ip INTEGER UNIQUE)")

    # Adds ip addres to the table if unique
    c.execute("INSERT OR IGNORE INTO ips VALUES (:ip)", {'ip': cleaned_ip})

    # Picks the id of the last ip aka amount
    c.execute("SELECT rowid FROM ips ORDER BY rowid DESC LIMIT 1")

    # Strips that item of everything except number
    last_item = c.fetchall()
    amount_of_ips = number_cleaner(last_item)

    c.execute("SELECT * FROM ips")
    items = c.fetchall()

    conn.commit()
    conn.close()
    return amount_of_ips

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    ip=request.headers.get('X-Forwarded-For', request.remote_addr)
    total_ips = float(ip_counter(ip))
    one_person_value = 20
    opacity = int(total_ips * one_person_value)
    return render_template('index.html', opacity=opacity)

if __name__ == '__main__':
    app.run(debug=False)


