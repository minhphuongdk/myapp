# -*- coding: utf-8 -*-
from flask import Flask,request
from flask import render_template
# from image import *
from database import *
import random
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
connect=database('iphone.db')
name=''
app = Flask(__name__, static_url_path = "",static_folder = "templates")
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/macos/Desktop/Mega/MEGA/app1/chat.db'
db=SQLAlchemy(app)
# comment
class History(db.Model):
  id=db.Column('id',db.Integer,primary_key=True)
  message=db.Column('message',db.String(500))
@socketio.on('message')
def handleMessage(msg):
  print('Message: ' + msg)
  message=History(message=msg)
  db.session.add(message)
  db.session.commit()
  send(msg, broadcast=True)

@app.route('/admin',methods=['POST','GET'])
def admin():
    if request.method=="POST":
        file_get=open('id.txt','r')
        file_id=file_get.read().replace(' ','').replace('\n','')
        file_get.close()
        pic=request.form['pic']
        name=request.form['name']
        info=request.form['info']
        price=request.form['price']
        status=request.form['status']
        name_save="{name:'"+name+"'"+','
        id_save="id:'"+file_id+"',"
        pic_save="pic:'"+pic+"',"
        info_save="info:'"+info+"',"
        status_save="status:'"+status+"',"
        price_save="price:'"+price+"'},"
        product=name_save+id_save+pic_save+info_save+status_save+price_save
        file=open('product.txt','a',encoding='utf-8')
        file.write(product)
        connect.insert(name,info,status,price,pic)
        file_id=int(file_id)+1
        file_get=open('id.txt','w')
        file_get.write(str(file_id))
        file_get.close()
        return render_template('admin/index.html')
    else:
         return render_template('admin/index.html')
@app.route('/admin/giao-luu',methods=['POST','GET'])
def giaoluu():
          if request.method=='POST':
              file=str(open('detail.txt','r').read()).split('\n')
              item=file[int(request.form['index'])]+'\n'
              file=str(open('detail.txt','r').read()).replace(item,'')
              f=open('detail.txt','w',encoding='utf-8').write(file)
              connect.delete(int(request.form['index'])+1)
          file=open('detail.txt','r')
          file=file.read()
          return render_template('admin/giaoluu.html',details=file)         
@app.route('/',methods=['POST','GET'])
def trangchu():
        messages=History.query.all()
        file=open('product.txt','r',encoding='utf-8')
        file=file.read()
        if request.method=="POST":
             get_id=request.form['get']
             result=connect.find(int(get_id))
             global name
             name=result[0]
             info=result[1]
             status=result[2]
             price=result[3]
             pic=result[4]
             new_price=int(price.replace('.',''))
             return render_template('home/convert.html',name=name,info=info,status=status,price=price,pic=pic,new_price=new_price)
        else:    
             return render_template('home/home.html',product=file,messages=messages)


@app.route('/step-1',methods=['POST','GET'])
def stepone():
           if request.method=="POST":
               count=request.form['count']
               product_name=request.form['product_name']
               return render_template('home/step1.html',count=count,product_name=product_name,name=name)
           else:    
               return "Bạn chưa chọn sản phẩm để chuyển đổi"
@app.route('/step-2',methods=['POST','GET'])
def steptwo():
    if request.method=="POST":
           name=request.form['fullname']
           place=request.form['place']
           phone=request.form['phone']
           detail=request.form['detail']
           result=request.form['result']
           connect.add(name,place,phone,detail,result,False)
           file=open('detail.txt','a',encoding='utf-8')
           name_save="{name:'"+name+"'"+','
           place_save="place:'"+place+"',"
           phone_save="phone:'"+phone+"',"
           detail_save="detail:'"+detail+"',"
           result_save="result:'"+result+"'},"
           details_save=name_save+place_save+phone_save+detail_save+result_save+'\n'
           file.write(details_save)
           return  render_template('home/step2.html',nofi="Giao dịch hoàn tất")  
# @app.route('/chat')
# def chat():
#      messages=History.query.all()
#      return render_template('home/chat.html',messages=messages)
if __name__== '__main__':
  # app.run(debug=True,port=5000)
  socketio.run(app)	
  
