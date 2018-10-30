import sqlite3
import uuid
class database:
		def __init__(self,db):
			self.con=sqlite3.connect(db,check_same_thread=False,timeout=10)
			self.cur=self.con.cursor()
			self.cur.execute("CREATE TABLE IF NOT EXISTS iphone (id INTEGER PRIMARY KEY,name text,info text,status text,price text,pic text)")
			self.cur.execute("CREATE TABLE IF NOT EXISTS detail (id INTEGER PRIMARY KEY,name text,place text,phone text,model text,detail text,result text)")
			self.cur.execute("CREATE TABLE IF NOT EXISTS hot (id INTEGER PRIMARY KEY, name text, count int) ")
			self.cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,name text, email text, password text,status boolean)")
			self.cur.execute("CREATE TABLE IF NOT EXISTS buy (id INTEGER PRIMARY KEY,b_name text,b_phone text,b_sex text,b_job text,b_place text,b_location text,b_pay text,b_info text,b_time text)")
			self.cur.execute("CREATE TABLE IF NOT EXISTS hangxi (id INTEGER PRIMARY KEY,name text,info text,pic text,price text,myprice text,status text,limits text)")
			self.cur.execute("CREATE TABLE IF NOT EXISTS hx_detail (id INTEGER PRIMARY KEY,hx_name text,hx_phone text,hx_place text,hx_location text,hx_pay text,hx_time text,hx_count text)")
			# self.cur.execute("CREATE TABLE IF NOT EXISTS sessions(id INTEGER PRIMARY KEY,email text,session text)")
			self.con.commit()
		def insert(self,name,info,status,price,pic):
			self.cur.execute("INSERT INTO iphone VALUES(NULL,?,?,?,?,?)",(name,info,status,price,pic))
			self.con.commit()
		def insert_user(self,name,email,password,status):
			self.cur.execute("INSERT INTO users VALUES(NULL,?,?,?,?)",(name,email,password,status))
			self.con.commit()	
		def find_insert_user(self,email):
		              self.cur.execute("SELECT email FROM users WHERE email=? ",(email,))
		              rows=self.cur.fetchall()
		              return rows
		def find_pwd(self,password,email):
		              self.cur.execute("SELECT * FROM users WHERE password=? and email=? ",(password,email))
		              rows=self.cur.fetchall()
		              return rows
		def get_name(self,password,email):
		              self.cur.execute("SELECT name FROM users WHERE password=? and email=? ",(password,email))
		              rows=self.cur.fetchall()
		              return rows          
		def update_status(self,status,email):
		              self.cur.execute("UPDATE users SET status=? WHERE email=?",(status,email))
		              self.con.commit()
		def check_status(self,email):
		              self.cur.execute("SELECT status FROM users WHERE email=?",(email,))
		              rows=self.cur.fetchone()
		              return rows
		def add_sessions(self,email,session):
			self.cur.execute("INSERT INTO sessions VALUES(NULL,?,?)",(email,session))
			self.con.commit()
		def check_sessions(self,email):
			self.cur.execute("SELECT email FROM sessions WHERE email=?",(email,))
			rows=self.cur.fetchall()
			return rows	
		def query_all_status(self,status):
		              self.cur.execute("SELECT email FROM users WHERE status =?",(status,))
		              rows=self.cur.fetchall()
		              return rows                                                       
		def find(self,id):
			self.cur.execute("SELECT * FROM iphone WHERE id=? ",(id,)) 
			rows=self.cur.fetchall()
			rows=str(rows).split(', ')
			name=rows[1].replace("'","")
			info=rows[2].replace("'","")
			status=rows[3].replace("'","")
			price=rows[4].replace("'","")
			pic=rows[5].replace("'","").replace(')]','')
			return name,info,status,price,pic
		def find_hangxi(self,id):
			self.cur.execute("SELECT * FROM hangxi WHERE id=? ",(id,)) 
			rows=self.cur.fetchall()
			rows=str(rows).split(', ')
			name=rows[1].replace("'","")
			info=rows[2].replace("'","")
			pic=rows[3].replace("'","")
			price=rows[4].replace("'","")
			myprice=rows[5].replace("'","")
			status=rows[6].replace("'","")
			limit=rows[7].replace("'","").replace(')]','')
			return name,info,pic,price,myprice,status,limit	
		def find_name(self,name):
			self.cur.execute("SELECT * FROM iphone WHERE name=? ",(name,)) 
			rows=self.cur.fetchall()
			rows=str(rows).split(', ')
			name=rows[1].replace("'","")
			info=rows[2].replace("'","")
			status=rows[3].replace("'","")
			price=rows[4].replace("'","")
			pic=rows[5].replace("'","").replace(')]','')
			return name,info,status,price,pic	
		def add(self,name,place,phone,model,detail,result):
			self.cur.execute("INSERT INTO detail VALUES(NULL,?,?,?,?,?,?)",(name,place,phone,model,detail,result))
			self.con.commit()
		def add_hangxi(self,name,info,pic,price,myprice,status,limits):
			self.cur.execute("INSERT INTO hangxi VALUES(NULL,?,?,?,?,?,?,?)",(name,info,pic,price,myprice,status,limits))
			self.con.commit()
		def add_hx_detail(self,hx_name,hx_phone,hx_place,hx_location,hx_pay,hx_time,hx_count):
			self.cur.execute("INSERT INTO hx_detail VALUES(NULL,?,?,?,?,?,?,?)",(hx_name,hx_phone,hx_place,hx_location,hx_pay,hx_time,hx_count))
			self.con.commit()			
		def add_buy(self,b_name,b_phone,b_sex,b_job,b_place,b_location,b_pay,b_info,b_time):
			self.cur.execute("INSERT INTO buy VALUES(NULL,?,?,?,?,?,?,?,?,?)",(b_name,b_phone,b_sex,b_job,b_place,b_location,b_pay,b_info,b_time))
			self.con.commit()	
		def delete(self,id):
		              self.cur.execute("DELETE FROM detail WHERE id=?",(id,))
		              self.con.commit()
		def buy_delete(self,id):
		              self.cur.execute("DELETE FROM buy WHERE id=?",(id,))
		              self.con.commit()
		def hx_delete(self,id):
		              self.cur.execute("DELETE FROM hx_detail WHERE id=?",(id,))
		              self.con.commit()                                       
		def count(self,model):
		               self.cur.execute(" SELECT count(*) FROM detail WHERE model = ?",(model,))
		               row=int(str(self.cur.fetchall()).replace('[(','').replace(',)]',''))
		               return row
		def add_count(self,name,count):
		                self.cur.execute(" INSERT INTO hot VALUES(NULL,?,?)",(name,count))
		                self.con.commit()
		def find_add_count(self,name):
			  self.cur.execute("SELECT name FROM hot WHERE name=?",(name,))
			  row=self.cur.fetchall()
			  return row
		def update_count(self,count,name):
		                 self.cur.execute("UPDATE hot SET count=? WHERE name=?",(count,name)) 
		                 self.con.commit()
		# def __del__(self):
		#                 self.con.close()                                             
		# def search(self,id):
		#                self.cur.execute("SELECT status FROM detail WHERE id=?",(id,))
		#                rows=cur.fetchall()
		#                return rows
		# def update(self,status,id):

# def session(string_length):
#     random = str(uuid.uuid4())
#     random = random.upper() 
#     random = random.replace("-","") 
#     return random[0:string_length] 
    

# session=session(30)
# print(session)