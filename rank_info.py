import sqlite3
from database import *
connect=database('iphone.db')
def item():
	con=sqlite3.connect('iphone.db')
	cur=con.cursor()
	cur.execute("SELECT name FROM hot GROUP BY id ORDER BY count DESC  LIMIT 4 ")
	rows=cur.fetchall()
	item1=str(rows[0]).replace("('","").replace("',)","")
	item2=str(rows[1]).replace("('","").replace("',)","")
	item3=str(rows[2]).replace("('","").replace("',)","")
	item4=str(rows[3]).replace("('","").replace("',)","")
	return item1,item2,item3,item4
item1=item()[0]
item2=item()[1]
item3=item()[2]
item4=item()[3]
name1=connect.find_name(item1)
name2=connect.find_name(item2)
name3=connect.find_name(item3)
name4=connect.find_name(item4)
my_item1='{name:'+"'"+name1[0]+"'"+","+'info:'+"'"+name1[1]+"'"+","+'status:'+"'"+name1[2]+"'"+","+'price:'+"'"+name1[3]+"'"+","+'pic:'+"'"+name1[4]+"'"+'},'
my_item2='{name:'+"'"+name2[0]+"'"+","+'info:'+"'"+name2[1]+"'"+","+'status:'+"'"+name2[2]+"'"+","+'price:'+"'"+name2[3]+"'"+","+'pic:'+"'"+name2[4]+"'"+'},'
my_item3='{name:'+"'"+name3[0]+"'"+","+'info:'+"'"+name3[1]+"'"+","+'status:'+"'"+name3[2]+"'"+","+'price:'+"'"+name3[3]+"'"+","+'pic:'+"'"+name3[4]+"'"+'},'
my_item4='{name:'+"'"+name4[0]+"'"+","+'info:'+"'"+name4[1]+"'"+","+'status:'+"'"+name4[2]+"'"+","+'price:'+"'"+name4[3]+"'"+","+'pic:'+"'"+name4[4]+"'"+'},'
file_hot=my_item1+my_item2+my_item3+my_item4
