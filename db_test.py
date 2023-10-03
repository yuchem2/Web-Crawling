import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='2038094', db='courseDB', charset='utf8')

cur = conn.cursor()

td = [11, 'a', 'b', 'c']
# cur.execute("INSERT INTO test VALUES(%s, %s)", td[:2])
# cur.execute("SELECT id FROM test where id = %s and name = %s", (td[0], td[1]))
cur.execute("SELECT id FROM test where id = %s", "12")
res = cur.fetchall()
print(len(res))
conn.commit()
conn.close()
