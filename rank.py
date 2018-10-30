
import sqlite3
from database import *
connect=database('iphone.db')
class rank:
	def __init__(self,model,check):
		if str(connect.find_add_count(model)) == '[]' :
		          connect.add_count(model,int(check))
		else:
			connect.update_count(int(check),model)


