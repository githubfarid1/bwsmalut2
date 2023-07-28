from datetime import datetime, timedelta
import fitz
import os

fileinfolist = []
allfilelist = [os.path.join(root, file) for root, dirs, files in os.walk(os.path.join("/home/farid/pdfs/alihmedia_inactive/")) for file in files if file.endswith(".pdf")]
for filepath in allfilelist:
    infotime = os.path.getmtime(filepath)
    infodate = datetime.fromtimestamp(infotime).strftime('%d-%m-%Y')
    mdict = {
        "file": filepath,
        "date": infodate,
        "pages": fitz.open(filepath).page_count
    }
    fileinfolist.append(mdict)

num_of_dates = 30
start = datetime.today()
date_list = [start.date() - timedelta(days=x) for x in range(num_of_dates)]
date_list.sort()
docscan = []
doccolor = []
docdate = []
print(date_list)
for d in date_list:
    pages = 0
    for fl in fileinfolist:
        if fl['date'] == d.strftime('%d-%m-%Y'):
            pages += fl['pages']
    docdate.append(d.strftime('%d-%m-%Y'))
    docscan.append(pages)
    doccolor.append("rgba(112, 185, 239, 1)")

print(docdate, docscan)