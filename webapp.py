from logging import root
from urllib import request
from pip import main
from app import app
from flask import Flask,render_template,jsonify,request,send_file
from app.db import Session,engine
from app.models import *
from utils.functions import write_db_data_to_csv, get_all_data
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

try:
    sess = Session()
except Exception as e:
    print("|-| Error creating DB session... 🕯️")
    print(e)

@app.route("/")
@cache.cached(timeout=1)
def table():
    all_urls_from_db = sess.query(Url)
    all_forms_from_db = sess.query(Form)
    all_inputs_from_db = sess.query(Input)
    
    return render_template("index.html", 
        all_urls_from_db=all_urls_from_db, 
        all_forms_from_db=all_forms_from_db, 
        all_inputs_from_db=all_inputs_from_db)

@app.route("/api/urls")
@cache.cached(timeout=1)
def get_urls():
    all_urls_from_db = sess.query(Url)
    return render_template("urls.html", 
        all_urls_from_db=all_urls_from_db)

@app.route("/api/urls-forms-inputs")
@cache.cached(timeout=1)
def get_urls_forms_inputs():
    all_urls_from_db = sess.query(Url)
    all_forms_from_db = sess.query(Form)
    all_inputs_from_db = sess.query(Input)

    return render_template("urls-forms-inputs.html", 
        all_urls_from_db=all_urls_from_db, 
        all_forms_from_db=all_forms_from_db, 
        all_inputs_from_db=all_inputs_from_db)

@app.route("/download/csv")
@cache.cached(timeout=1)
def download_csv():
    csv_filename = "outputs/forms-data.csv"
    db_data = get_all_data(sess, Url, Form, Input)
    write_db_data_to_csv(db_data, csv_filename)

    return send_file(csv_filename,
                     mimetype='text/csv',
                     attachment_filename='forms-data.csv',
                     as_attachment=True)

'''
@app.route("/add-url", methods=['POST'])
def add_url():
    with engine.connect() as conn:
        url = request.form.get('url')
        new_url = Url(url=url)
        sess.add(new_url)

        try:
            sess.commit()
            sess.refresh()
        except:
            return jsonify({"response":"|-| Error. URL exists"})

    return jsonify({"response":"|+| URL added sucessfully"})
'''

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)