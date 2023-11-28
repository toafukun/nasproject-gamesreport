from __init__ import app
from flask import render_template, request, url_for
import sqlite3
from datetime import datetime
import os

DATABASE='database.db'
def save_picture(image_file):
 if image_file:
        if image_file:
         upload_folder = "saved_pictures"
         if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filename = os.path.join(upload_folder, image_file.filename)
        full_path = os.path.abspath(filename)
        image_file.save(full_path)
        return full_path

@app.route('/')
def index():
    return render_template(
        'index.html',
    )
    
    

@app.route('/reports', methods=['POST'])
def reports():
    password= request.form['password']
    if password == '2525':
        return render_template(
        'report.html')

    elif password == '8888':
         def get_reportgame_tables():
          con = sqlite3.connect(DATABASE)
          cursor = con.cursor()

          # sqlite_master テーブルをクエリして、テーブル名を取得
          cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
          all_tables = cursor.fetchall()

          con.close()

          # テーブル名の中から "reportgame_" で始まるものだけを取り出す
          reportgame_tables = [table[0] for table in all_tables if table[0].startswith("reportgame_")]
          

          return reportgame_tables
         list_tables=get_reportgame_tables()
         table0=list_tables[0]


         con = sqlite3.connect(DATABASE)
         db_data=con.execute(f'SELECT * FROM {table0}').fetchall()
         data={}
         for row in db_data:
          data.update({'content1':row[0],'content2':row[1],'filedata1':row[2],'filedata2':row[3],'filedata3':row[4],'filedata4':row[5]})
         con.close()
         print(data['filedata1'])
         return render_template('games_list.html',
          data=data)
    

    else:
            return render_template('missedpass.html')
    


@app.route('/recode', methods=['POST'])
def recode():
    content1 = request.form['content1']
    try:
     content2 = request.form['checklist1']
    except:
     content2='off'
    list_image_file = request.files.getlist('imagefiles')
    if len(list_image_file)==3:
       list_image_file+=[''] 
    elif len(list_image_file)==2:
     list_image_file+=['','']
    elif len(list_image_file)==4:
       pass
    elif len(list_image_file)==1:
     list_image_file+=['','','']
    else:
       list_image_file+=['','','','']

    time=datetime.now()
    
    filename1=save_picture(list_image_file[0])
    filename2=save_picture(list_image_file[1])
    filename3=save_picture(list_image_file[2])
    filename4=save_picture(list_image_file[3])
    
    input_data=[content1,content2,filename1,filename2,filename3,filename4]
    stred_time=time.strftime("%Y%m%d%H%M%S")
    table_name = "reportgame_" + str(stred_time)
    fields = ["content1", "content2", "filename1", "filename2", "filename3", "filename4"]
    con = sqlite3.connect(DATABASE)
    con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(fields)})")
    con.execute(f'INSERT INTO {table_name} VALUES(?, ?, ?, ?, ?, ?)' ,input_data)
    con.commit()
    con.close()
    return render_template('index.html')


     

