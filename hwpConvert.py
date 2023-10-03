import os
import olefile
import zlib
import struct

path = "G://자료파일//고려대(세종)//3학년 2학기//캡스톤 디자인2//downloads//hwp//"
out_path = "G://자료파일//고려대(세종)//3학년 2학기//캡스톤 디자인2//downloads//txt//"

listdir = os.listdir(path)
print(listdir)
for name in listdir:
    f = olefile.OleFileIO(path+name)
    dirs = f.listdir()

    header = f.openstream("FileHeader")
    header_data = header.read()
    is_compressed = (header_data[36] & 1) == 1

    nums = []
    for d in dirs:
        if d[0] == "BodyText":
            nums.append(int(d[1][len("Section"):]))
    sections = ["BodyText/Section"+str(x) for x in sorted(nums)]

    text = ""
    for section in sections:
        body_text = f.openstream(section)
        data = body_text.read()
        if is_compressed:
            unpacked_data = zlib.decompress(data, -15)
        else:
            unpacked_data = data

        section_text = ""
        i = 0
        size = len(unpacked_data)
        while i < size:
            header = struct.unpack_from("<I", unpacked_data, i)[0]
            rec_type = header & 0x3ff
            rec_len = (header >> 20) & 0xfff

            if rec_type in [67]:
                rec_data = unpacked_data[i+4:i+4+rec_len]
                section_text += rec_data.decode('utf-16')
                section_text += '\n'

            i += (4 + rec_len)

        text += section_text
        text += '\n'

    newfile = os.path.splitext(name)[0] + '.txt'
    out = open(out_path + newfile, 'w', encoding='UTF-16')
    out.write(text)
