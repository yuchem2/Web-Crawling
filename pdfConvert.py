import os
import fitz

path = "G://자료파일//고려대(세종)//3학년 2학기//캡스톤 디자인2//downloads//pdf//"
out_path = "G://자료파일//고려대(세종)//3학년 2학기//캡스톤 디자인2//downloads//txt//"
listdir = os.listdir(path)

for file in listdir:
    doc = fitz.open(path+file)
    newfile = os.path.splitext(file)[0] + '.txt'
    f = open(out_path + newfile, 'w', encoding='UTF-16')
    for page in doc:
        text = page.get_text()
        f.write(text)
