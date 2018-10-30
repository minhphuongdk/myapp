<<<<<<< HEAD
# -*- coding: utf-8 -*-
from flask import Flask,request,session
from flask import render_template
import os
# from image import *
from database import *
import random
from rank_info import *
from rank import *
connect=database('iphone.db')
name=''
email=''
app = Flask(__name__, static_url_path = "",static_folder = "templates")
app.secret_key=os.urandom(24)
@app.route('/administrator',methods=['POST','GET'])
def admin():
    if request.method=="POST":
      if request.form['submit']=='myproduct':  
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
      elif request.form['submit']=='hangxi':
        name=request.form['name']
        info=request.form['info']
        pic=request.form['pic']
        price=request.form['price']
        myprice=request.form['myprice']
        status=request.form['status']
        limit=request.form['limit']
        connect.add_hangxi(name,info,pic,price,myprice,status,limit)
        name_save="{name:'"+name+"'"+','
        info_save="info:'"+info+"',"
        pic_save="pic:'"+pic+"',"
        price_save="price:'"+price+"',"
        myprice_save="myprice:'"+myprice+"',"
        status_save="status:'"+status+"',"
        limit_save="limit:'"+limit+"'},"
        hangxi=name_save+info_save+pic_save+price_save+myprice_save+status_save+limit_save
        file=open('hangxi.txt','a',encoding='utf-8')
        file.write(hangxi)
        file.close()
        return render_template('admin/index.html')
    else:
         return render_template('admin/index.html')
@app.route('/administrator/giao-luu',methods=['POST','GET'])
def giaoluu():
          if request.method=='POST':
              file=str(open('detail.txt','r',encoding='utf-8').read()).split('\n')
              item=file[int(request.form['index'])]+'\n'
              file=str(open('detail.txt','r',encoding='utf-8').read()).replace(item,'')
              f=open('detail.txt','w',encoding='utf-8').write(file)
              connect.delete(int(request.form['index'])+1)
          file=open('detail.txt','r',encoding='utf-8')
          file=file.read()
          return render_template('admin/giaoluu.html',details=file)
@app.route('/administrator/buy',methods=['POST','GET'])
def buy():
          if request.method=='POST':
              file=str(open('buy.txt','r',encoding='utf-8').read()).split('\n')
              item=file[int(request.form['index'])]+'\n'
              file=str(open('buy.txt','r',encoding='utf-8').read()).replace(item,'')
              f=open('buy.txt','w',encoding='utf-8').write(file)
              connect.buy_delete(int(request.form['index'])+1)
          file=open('buy.txt','r',encoding='utf-8')
          file=file.read()
          return render_template('admin/buy.html',buy=file)
@app.route('/administrator/hangxi',methods=['POST','GET'])
def hangxi():
          if request.method=='POST':
              file=str(open('hx_detail.txt','r',encoding='utf-8').read()).split('\n')
              item=file[int(request.form['index'])]+'\n'
              file=str(open('hx_detail.txt','r',encoding='utf-8').read()).replace(item,'')
              f=open('hx_detail.txt','w',encoding='utf-8').write(file)
              connect.hx_delete(int(request.form['index'])+1)
          file=open('hx_detail.txt','r',encoding='utf-8')
          file=file.read()
          return render_template('admin/hangxi.html',hangxi=file)                              
@app.route('/',methods=['POST','GET'])
def trangchu():
        global email
        main_product=open('product.txt','r',encoding='utf-8')
        main_product=main_product.read()
        hangxi=open('hangxi.txt','r',encoding='utf-8')
        hangxi=hangxi.read()
        global name
        if request.method=="POST":
            if request.form['submit']=='product':
             get_id=request.form['get']
             result=connect.find(int(get_id))
             name=result[0]
             info=result[1]
             status=result[2]
             price=result[3]
             pic=result[4]
             new_price=int(price.replace('.',''))
             return render_template('home/convert.html',name=name,info=info,status=status,price=price,pic=pic,new_price=new_price)
            elif request.form['submit']=='product_hot':
              get_name=request.form['get_hot']
              result=connect.find_name(get_name)
              name=result[0]
              info=result[1]
              status=result[2]
              price=result[3]
              pic=result[4]
              new_price=int(price.replace('.',''))
              return render_template('home/convert.html',name=name,info=info,status=status,price=price,pic=pic,new_price=new_price)
            elif request.form['submit']=='login':
              email=request.form['email']
              password=request.form['pwd']
              if len(connect.find_insert_user(email))==0:
                  return render_template('home/aleft.html',aleft="Tài khoản không tồn tại !")
              elif len(connect.find_pwd(password,email)) != 0:
                   connect.update_status(True,email)
                   session['user']=email
                   my_name=str(connect.get_name(password,email)).replace("[('","").replace("',)]","")
                   aleft='Xin chào'+' ' + my_name +'!'
                   return render_template('home/home.html',check_status=str(connect.check_status(email)),product=main_product,product_hot=file_hot,event_active='active',script="event_click",hangxi=hangxi,aleft=aleft)
              else: 
                  return render_template('home/aleft.html',aleft="Mật khẩu không chính xác!")
            elif request.form['submit']=='logout':
                   connect.update_status(False,email)
                   session.pop('user',None)
                   return render_template('home/home.html',product=main_product,product_hot=file_hot,hangxi=hangxi)
            elif request.form['submit']=='daugia':
                   return render_template('home/home.html',product=main_product,event_active='active',nofi='Thành công!',check_status=str(connect.check_status(email)),script="event_click'",hangxi=hangxi)
            elif request.form['submit']=='buy':
                   buy_name=request.form['buy_name']
                   buy_info=request.form['buy_info']
                   buy_price=request.form['buy_price']
                   return render_template('home/buy.html',buy_name=buy_name,buy_info=buy_info,buy_price=buy_price)
            elif request.form['submit']=='Hoàn tất':
                   b_name=request.form['b_name']
                   b_phone=request.form['b_phone']
                   b_sex=request.form['b_sex']
                   b_job=request.form['b_job']
                   b_place=request.form['b_place']
                   b_location=request.form['b_location']
                   b_pay=request.form['b_pay']
                   b_info=request.form['b_info']
                   b_time=request.form['b_time']
                   connect.add_buy(b_name,b_phone,b_sex,b_job,b_place,b_location,b_pay,b_info,b_time)
                   file=open('buy.txt','a',encoding='utf-8')
                   b_name_save="{b_name:'"+b_name+"'"+','
                   b_phone_save="b_phone:'"+b_phone+"',"
                   b_sex_save="b_sex:'"+b_sex+"',"
                   b_job_save="b_job:'"+b_job+"',"
                   b_place_save="b_place:'"+b_place+"',"
                   b_location_save="b_location:'"+b_location+"',"
                   b_pay_save="b_pay:'"+b_pay+"',"
                   b_info_save="b_info:'"+b_info+"',"
                   b_time_save="b_time:'"+b_time+"'},"
                   buy_save=b_name_save+b_phone_save+b_sex_save+b_job_save+b_place_save+b_location_save+b_pay_save+b_info_save+b_time_save+'\n'
                   file.write(buy_save)
                   file.close()
                   return render_template('home/home.html',product=main_product,product_hot=file_hot,hangxi=hangxi,check_status=str(connect.check_status(email)),aleft="Mua hàng thành công !")
            elif request.form['submit']=='hangxi':
                   get_id=request.form['hangxi_id']
                   result=connect.find_hangxi(int(get_id))
                   name=result[0]
                   info=result[1]
                   pic=result[2]
                   price=result[3]
                   myprice=result[4]
                   status=result[5]
                   limit=result[6]
                   num_limit=int(limit.replace('c trở lên',''))
                   return render_template('home/hangxi.html',name=name,info=info,pic=pic,price=price,myprice=myprice,status=status,limit=limit,num_limit=num_limit)
            elif request.form['submit']=='Xong':
                   hx_name=request.form['name']
                   hx_phone=request.form['phone']
                   hx_place=request.form['place']
                   hx_location=request.form['location']
                   hx_pay=request.form['pay']
                   hx_time=request.form['time']
                   hx_count=request.form['count']
                   connect.add_hx_detail(hx_name,hx_phone,hx_place,hx_location,hx_pay,hx_time,hx_count)
                   file=open('hx_detail.txt','a',encoding="utf-8")
                   hx_name_save="{hx_name:'"+hx_name+"'"+','
                   hx_phone_save="hx_phone:'"+hx_phone+"',"
                   hx_place_save="hx_place:'"+hx_place+"',"
                   hx_location_save="hx_location:'"+hx_location+"',"
                   hx_pay_save="hx_pay:'"+hx_pay+"',"
                   hx_time_save="hx_time:'"+hx_time+"',"
                   hx_count_save="hx_count:'"+hx_count+"'},"
                   hx_save=hx_name_save+hx_phone_save+hx_place_save+hx_location_save+hx_pay_save+hx_time_save+hx_count_save
                   file.write(hx_save)
                   return render_template('home/home.html',product=main_product,product_hot=file_hot,hangxi=hangxi,aleft="Đặt hàng thành công !",check_status=str(connect.check_status(email)))
            elif request.form['submit']=="showless":
                  return render_template('home/khosanpham.html',product=main_product)
            elif request.form['submit']=="gianhangxi":
                  return render_template('home/gianhangxi.html',hangxi=hangxi)
            elif request.form['submit']=='raovat':
                   return render_template('home/home.html',product=main_product,product_hot=file_hot,check_status=str(connect.check_status(email)),hangxi=hangxi,onload="openPage('raovat')" )
            elif request.form['submit']=='thongbao':
                   return render_template('home/home.html',product=main_product,product_hot=file_hot,check_status=str(connect.check_status(email)),hangxi=hangxi,onload="openPage('thongbao')" )
            elif request.form['submit']=='dangnhap':
                   return render_template('home/home.html',product=main_product,product_hot=file_hot,check_status=str(connect.check_status(email)),hangxi=hangxi,onload="openPage('dangnhap')" )                                                            
        else:
             if 'user' in session:
                return render_template('home/home.html',product=main_product,product_hot=file_hot,check_status=str(connect.check_status(email)),hangxi=hangxi)   
             else:
                return render_template('home/home.html',product=main_product,product_hot=file_hot,hangxi=hangxi)


@app.route('/step-1',methods=['POST','GET'])
def stepone():
           if request.method=="POST":
               count=request.form['count']
               product_name=request.form['product_name']
               return render_template('home/step1.html',count=count,product_name=product_name,name=name)
           else:    
               return render_template('home/aleft.html',aleft="Bạn chưa chọn sản phẩm để chuyển đổi")
@app.route('/step-2',methods=['POST','GET'])
def steptwo():
    if request.method=="POST":
           name=request.form['fullname']
           place=request.form['place']
           phone=request.form['phone']
           model=request.form['model']
           detail=request.form['detail']
           result=request.form['result']
           connect.add(name,place,phone,model,detail,result)
           check=connect.count(model)
           rank(model,check)
           file=open('detail.txt','a',encoding='utf-8')
           name_save="{name:'"+name+"'"+','
           place_save="place:'"+place+"',"
           phone_save="phone:'"+phone+"',"
           detail_save="detail:'"+detail+"',"
           result_save="result:'"+result+"'},"
           details_save=name_save+place_save+phone_save+detail_save+result_save+'\n'
           file.write(details_save)
           file.close()
           return  render_template('home/step2.html',nofi="Giao dịch hoàn tất")
@app.route('/dangky',methods=['POST','GET'])
def register():
  if request.method=="POST":
     name=request.form['name']
     email=request.form['email']
     password=request.form['pwd']
     if len(connect.find_insert_user(email))== 0:
         connect.insert_user(name,email,password,False)
         return render_template('home/aleft.html',aleft="Đăng ký thành công !")
     else:
         
         return render_template('home/aleft.html',aleft="Email đã có người sử dụng !")
  else:       
         return render_template('home/register.html')
# @app.route('/dangnhap',methods=['POST','GET']) 
# def login():
#        if request.method=='POST':
#         email=request.form['email']
#         password=request.form['pwd']
#         if len(connect.find_insert_user(email))==0:
#                   return 'Tai khoan khong ton tai'
#         elif connect.find_insert_user(email) == (connect.find_pwd(password)):
#                    connect.update_status(True,email)
#                    return "Dang nhap thanh cong"
#         else: 
#                   return 'Mat khau khong chinh xac!'
#        else:           
#         return render_template('home/login.html')
# @app.route('/hangxi<string:id>')
# def chitiet(id):
#      url='hangxi'+str(id)+'.html'
#      return render_template(url)
if __name__== '__main__':
  app.run(debug=True,port=5000)

  
=======
import time
from selenium import webdriver
import chromedriver_binary

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/xhtml');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
>>>>>>> aae8e0bd9bd44890ab8410e7555773fbd8af3a97
