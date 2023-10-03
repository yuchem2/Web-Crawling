import os
import docx2txt


def docx_to_txt(path, out_path, filename):
    text = docx2txt.process(path+filename).split('\n')
    newfile = os.path.splitext(filename)[0] + '.txt'
    f = open(out_path + newfile, 'w', encoding='UTF-16')
    for item in text:
        f.write(item + '\n')
    f.close()


path = "G://자료파일//고려대(세종)//3학년 2학기//캡스톤 디자인2//downloads//docx//"
out_path = "G://자료파일//고려대(세종)//3학년 2학기//캡스톤 디자인2//downloads//txt//"
listdir = os.listdir(path)
for name in listdir:
    docx_to_txt(path, out_path, name)
