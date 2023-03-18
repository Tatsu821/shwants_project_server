import os
import sys
import pymysql.cursors
from flask import Flask, render_template, jsonify, request, make_response, redirect, url_for, flash
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging
import glob
import datetime
import shutil

# CORS：Ajax通信するためのライブラリ
from flask_restful import Api, Resource
from random import *
from PIL import Image
from pathlib import Path
from io import BytesIO
import base64

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
SUMMER_FOLDER = './summer_files'
AUTUMN_FOLDER = './autumn_files'
WINTER_FOLDER = './winter_files'


AVATOR_IMAGE = './avatorImage'


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SUMMER_FOLDER'] = SUMMER_FOLDER
app.config['AUTUMN_FOLDER'] = AUTUMN_FOLDER
app.config['WINTER_FOLDER'] = WINTER_FOLDER

app.config['AVATOR_IMAGE'] = AVATOR_IMAGE

conn = pymysql.connect(
    host='mysql',
    port=3306,
    user=os.environ.get('MYSQL_USER'),
    password=os.environ.get('MYSQL_PASSWORD'),
    db=os.environ.get('MYSQL_DATABASE'),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def select_all():
    # with conn.cursor() as cur:
    #     sql = "SELECT * FROM Images"
    #     cur.execute(sql)
    #     results = cur.fetchall()

    # return jsonify(results)
    l = glob.glob('./uploads/*.jpeg')
    return l


@app.route('/upload', methods=['POST'])
def upload_file():
    now = datetime.datetime.now()
    # logging.debug("warning")
    if request.method == 'POST':
        #     # logging.debug("warning")
        #     # check if the post request has the file part
        #     # if 'File' not in request.files:
        #     #     flash('No file part')
        #     #     return redirect(request.url)
        img = request.files["image"]
        season = request.form["season"]
        name = now.strftime('%Y%m%d_%H%M%S') + img.filename
        foldername = str(season)

        if foldername == "summer":
            path = os.path.join(app.config['SUMMER_FOLDER'], name)
            img.save(path)
        elif foldername == "autumn":
            path = os.path.join(app.config['AUTUMN_FOLDER'], name)
            img.save(path)
        elif foldername == "winter":
            path = os.path.join(app.config['WINTER_FOLDER'], name)
            img.save(path)
        elif foldername == "about":
            path = os.path.join(app.config['UPLOAD_FOLDER'], name)
            img.save(path)
        # path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        # img.save(path)
        return foldername
    #     # If the user does not select a file, the browser submits an
    #     # empty file without a filename.
    #     if file.name == '':
    #         flash('No selected file')
    #         return redirect(request.url)
    #     if file and allowed_file(file.name):
    #         filename = secure_filename(file.name)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #         return redirect(url_for('download_file', name=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/download', methods=['GET'])
def download_file():
    with conn.cursor() as cur:
        sql = f"INSERT INTO Images (title) Value (%(title)s)"
        cur.execute(sql, {'title': 'kome'})
        # cur.execute(sql)
    return "addddd"


@app.route('/delete', methods=['POST'])
def delete_file():
    if request.method == 'POST':
        data = request.get_data()
        path_data = str(data).split("'")[1]
        del_path = path_data.split('.')[0] + '.' + path_data.split('.')[2]
        # print(del_path)
        os.remove('./uploads/' + str(del_path))
        return request.get_data()


@app.route('/addAvator', methods=['GET','POST'])
def update_avator():
    now = datetime.datetime.now()
    # logging.debug("warning")
    if request.method == 'POST':
        shutil.rmtree('./avatorImage/')
        os.mkdir('avatorImage')
        #     # logging.debug("warning")
        #     # check if the post request has the file part
        #     # if 'File' not in request.files:
        #     #     flash('No file part')
        #     #     return redirect(request.url)
        img = request.files["image"]
        name = now.strftime('%Y%m%d_%H%M%S') + img.filename
        path = os.path.join(app.config['AVATOR_IMAGE'], name)
        img.save(path)
        return "success"

    elif request.method == 'GET':
        l = glob.glob('./avatorImage/*.jpeg')
        return l
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/summer/get', methods=['GET'])
def summer_get():
    # with conn.cursor() as cur:
    #     sql = "SELECT * FROM Images"
    #     cur.execute(sql)
    #     results = cur.fetchall()

    # return jsonify(results)
    l = glob.glob('./summer_files/*.jpeg')
    return l

@app.route('/summer/delete', methods=['POST'])
def summer_delete():
    if request.method == 'POST':
        data = request.get_data()
        path_data = str(data).split("'")[1]
        del_path = path_data.split('.')[0] + '.' + path_data.split('.')[2]
        # print(del_path)
        os.remove('./summer_files/' + str(del_path))
        return request.get_data()

@app.route('/autumn/get', methods=['GET'])
def autumn_get():
    # with conn.cursor() as cur:
    #     sql = "SELECT * FROM Images"
    #     cur.execute(sql)
    #     results = cur.fetchall()

    # return jsonify(results)
    l = glob.glob('./autumn_files/*.jpeg')
    return l

@app.route('/autumn/delete', methods=['POST'])
def autumn_delete():
    if request.method == 'POST':
        data = request.get_data()
        path_data = str(data).split("'")[1]
        del_path = path_data.split('.')[0] + '.' + path_data.split('.')[2]
        # print(del_path)
        os.remove('./autumn_files/' + str(del_path))
        return request.get_data()

@app.route('/winter/get', methods=['GET'])
def winter_get():
    # with conn.cursor() as cur:
    #     sql = "SELECT * FROM Images"
    #     cur.execute(sql)
    #     results = cur.fetchall()

    # return jsonify(results)
    l = glob.glob('./winter_files/*.jpeg')
    return l

@app.route('/winter/delete', methods=['POST'])
def winter_delete():
    if request.method == 'POST':
        data = request.get_data()
        path_data = str(data).split("'")[1]
        del_path = path_data.split('.')[0] + '.' + path_data.split('.')[2]
        # print(del_path)
        os.remove('./winter_files/' + str(del_path))
        return request.get_data()

@app.route('/favorite/upload', methods=['POST'])
def favorite_upload():
    if request.method == 'POST':
        namedata = request.form["filename"]
        seasondata = request.form["season"]
        season = str(seasondata)
        path_data = str(namedata)
        filename = path_data.split('.')[0] + '.' + path_data.split('.')[2]

        if season == "summer":
            shutil.copy('./summer_files/' + filename, './favorite_files')
        elif season == "autumn":
            shutil.copy('./autumn_files/' + filename, './favorite_files')
        elif season == "winter":
            shutil.copy('./winter_files/' + filename, './favorite_files')
        elif season == "about":
            shutil.copy('./uploads/' + filename, './favorite_files')

        # path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        # img.save(path)
        return [filename, season]

@app.route('/favorite/get', methods=['GET'])
def favorite_get():
    # with conn.cursor() as cur:
    #     sql = "SELECT * FROM Images"
    #     cur.execute(sql)
    #     results = cur.fetchall()

    # return jsonify(results)
    l = glob.glob('./favorite_files/*.jpeg')
    return l

@app.route('/favorite/delete', methods=['POST'])
def favorite_delete():
    if request.method == 'POST':
        data = request.get_data()
        path_data = str(data).split("'")[1]
        del_path = path_data.split('.')[0] + '.' + path_data.split('.')[2]
        # print(del_path)
        os.remove('./favorite_files/' + str(del_path))
        return request.get_data()