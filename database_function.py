#coding=utf-8
import pymysql as pyms

#数据库连接信息
#db_config = {"host":"localhost","user":"root","password":"886655","data_base":"AshareDayPrices","port":3306}


#连接数据库
def db_connect(db_config):
	db = pyms.connect(host= db_config["host"],user=db_config["user"],password=db_config["password"],db=db_config["data_base"],port=db_config["port"],charset="utf8mb4")
	cur = db.cursor()
	print("连接数据库成功...")
	return db,cur

#查询操作
def db_select(cur,sql):
	#执行操作
	try:
		cur.execute(sql)
		results = cur.fetchall()
		return results
		print ("数据库查询操作成功..")
	#抛出异常
	except Exception as e:
		raise e
		print("数据库查询操作失败..")
	finally:
		print ("查询完成..")
#插入操作
def db_insert(db,cur,sql):
	#执行操作
	try:
		cur.execute(sql)
		db.commit()
		print("插入成功..")
	#错误回滚
	except Exception as e:
		print("插入失败..")
		print (e)
		db.rollback()
	finally:
		print("...")

		
# 批量插入
# sql是插入语句，parames是[(),(),...]
def db_many_insert(db,cur,sql,parames):
	#执行操作
	try:
		cur.executemany(sql,parames)
		db.commit()
		print("批量插入成功..")
	#错误回滚
	except Exception as e:
		print("批量插入失败..")
		print (e)
		db.rollback()
	finally:
		print("...")



def db_update(db,cur,sql):
	#执行更新
	try:
		cur.execute(sql)
		db.commit()
		print ("更新成功..")

	#错误回滚
	except Exception as e:
		print ("异常...")
		db.rollback()
	finally:
		print ("更新结束..")

def db_delete(db,cur,sql):
	try:
		cur.execute(sql)
		db.commit()
	except Exception as e:
		db.rollback()

	finally:
		print ("删除结束..")

def db_connection_close(db,cur):
	cur.close()
	db.close()
	print ("连接关闭..")




"""

###############数据库函数测试##############
print (type(db_config["host"]))

db,cur = db_connect(db_config)

sele_sql = "select * from asharebalancesheet t where  t.id ='00000120000630'"

insert_sql = "insert into test(id,code) values('111','222')"

update_sql = "update test set code=%s where id=%s" % ("333","111")

delete_sql = "delete from test where id =%s"%(111)


#查询测试
result = db_select(cur,sele_sql)

#插入测试
db_insert(db,cur,insert_sql)

#更新测试
db_update(db,cur,update_sql)

#删除测试
db_delete(db,cur,delete_sql)

print (result)

#关闭连接
db_connection_close(db, cur)

"""


