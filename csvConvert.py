import csv
import pymysql

path = "G://자료파일//고려대(세종)//3학년 2학기//캡스톤 디자인2//downloads//books.csv"
f = open(path, 'r')

reader = csv.reader(f)
conn = pymysql.connect(host='127.0.0.1', user='root', password='2038094', db='courseDB', charset='utf8')
cur = conn.cursor()
for line in reader:
    print(line)
    cur.execute("SELECT bookID FROM book WHERE bookname = %s", line[2])
    res = cur.fetchall()
    print(len(res))
    if len(res) == 0:
        print("----")
        cur.execute("INSERT INTO book (bookname, author, published) VALUES(%s, %s, %s)",
                    (line[2], line[3], line[4]))
        conn.commit()
        cur.execute("SELECT MAX(bookID) FROM book")
        res = cur.fetchall()
        bookId = res[-1][-1]
    else:
        print("=====")
        bookId = res[-1][-1]

    cur.execute("SELECT ID FROM course WHERE courseID = %s AND subID = %s", (line[0], line[1]))
    res = cur.fetchall()
    print(res)
    courseId = res[-1][-1]

    cur.execute("INSERT INTO course_book (bookID, courseID) VALUES(%s, %s)", (bookId, courseId))
    conn.commit()


