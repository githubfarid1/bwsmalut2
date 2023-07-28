from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Bundle, Doc, Department
from django.contrib import messages
import os
from django.db.models import Q
from os.path import exists
from django.conf import settings
import inspect
import sys
import time
from datetime import datetime, timedelta
import fitz

def getmenu():
    return Department.objects.all()

def getdata(method, parquery):
    query = ""
    if method == "GET":
        query = parquery

    isfirst = True
    boxlist = []

    #get caller function name
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    link = calframe[1][3] 
    d = Department.objects.get(link=link)
    if query == None or query == '':
        docs = Doc.objects.filter(bundle__department_id__exact=d.id)
    else:
        docs = Doc.objects.filter(Q(bundle__department_id__exact=d.id) & (Q(description__icontains=query)  | Q(bundle__title__icontains=query) | Q(bundle__year__contains=query)))
    isfirst = True
    curbox_number = ""
    curbundle_number = ""
    
    for ke, doc in enumerate(docs):
        path = os.path.join(settings.PDF_LOCATION, __package__.split('.')[0], d.link, str(doc.bundle.box_number), str(doc.doc_number) + ".pdf")
        pdffound = False
        filesize = 0
        pagecount = 0
        coverfilename = ""
        if exists(path):
            pdffound = True
            coverfilename = "{}_{}_{}_{}.png".format(__package__.split('.')[0], d.link, doc.bundle.box_number, doc.doc_number)
            # generatecover(pdffile=path, coverfilename=coverfilename)
            # filesize = get_size(path, "kb")
            # pagecount = get_page_count(pdffile=path)
        if isfirst:
            isfirst = False

            curbox_number = doc.bundle.box_number
            boxlist.append({
                "box_number": doc.bundle.box_number,
                "bundle_number": doc.bundle.bundle_number,
                "doc_number": doc.doc_number,
                "bundle_code": doc.bundle.code,
                "bundle_title": doc.bundle.title,
                "bundle_year": doc.bundle.year,
                "doc_description": doc.description,
                "doc_count": doc.doc_count,
                "bundle_orinot": doc.bundle.orinot,
                "row_number": ke + 1,
                "pdffound": pdffound,
                "doc_id": doc.id,
                "coverfilepath": os.path.join(settings.COVER_URL, coverfilename),
                "filesize": doc.filesize,
                "pagecount": doc.page_count,
            })
            continue
        if curbox_number == doc.bundle.box_number:
            box_number = ""
        else:
            box_number = doc.bundle.box_number
            curbox_number = doc.bundle.box_number
        
        if curbundle_number == doc.bundle.bundle_number:
            bundle_number = ""
            bundle_code = ""
            bundle_title = ""
            bundle_year = ""
            bundle_orinot = ""
        else:
            bundle_number = doc.bundle.bundle_number
            curbundle_number = doc.bundle.bundle_number
            bundle_code = doc.bundle.code
            bundle_title = doc.bundle.title
            bundle_year = doc.bundle.year
            bundle_orinot = doc.bundle.orinot
        
        doc_number = doc.doc_number
        doc_description = doc.description
        doc_count = doc.doc_count
        boxlist.append({
            "box_number": box_number,
            "bundle_number": bundle_number,
            "doc_number": doc_number,
            "bundle_code": bundle_code,
            "bundle_title": bundle_title,
            "bundle_year": bundle_year,
            "doc_description": doc_description,
            "doc_count": doc_count,
            "bundle_orinot": bundle_orinot,
            "row_number": ke + 1,
            "pdffound": pdffound,
            "doc_id": doc.id,
            "coverfilepath": os.path.join(settings.COVER_URL, coverfilename),
            "filesize": doc.filesize,
            "pagecount": doc.page_count,
        })
        
    isfirst = True
    rowbox = 0
    rowbundle = 0
    boxspan = 1
    bundlespan = 1      
    for ke, box in enumerate(boxlist):
        if isfirst:
            isfirst = False
            rowbox = ke
            rowbundle = ke
            boxspan = 1
            bundlespan = 1      
            continue
        if box['box_number'] == "":
            boxspan += 1
        else:
            boxlist[rowbox]['boxspan'] = boxspan
            boxspan = 1
            rowbox = ke

        if box['bundle_number'] == "":
            bundlespan += 1
        else:
            boxlist[rowbundle]['bundlespan'] = bundlespan
            bundlespan = 1
            rowbundle = ke

    # for last record
    if docs.count() != 0:
        boxlist[rowbox]['boxspan'] = boxspan
        boxlist[rowbundle]['bundlespan'] = bundlespan

    return boxlist

def summarydata(data):
    sumscan = 0
    listyear = []
    for d in data:
        if d['bundle_year'] is not None and d['bundle_year'].strip() != '':
            listyear.append(d['bundle_year'])
        if d['pdffound'] == True:
            sumscan += 1
    unyears = list(set(listyear))
    # tes = unyears.sort()
    unyears.sort()
    unyearstr = ", ".join(unyears)
    sumnotscan = len(data) - sumscan
    try:
        percent = sumscan / len(data) * 100
    except:
        percent = 0

    return (len(data), sumscan, sumnotscan, percent, unyearstr )

def irigasi(request):
    funcname = sys._getframe().f_code.co_name
    data = getdata(method=request.method, parquery=request.GET.get("search"))
    summary = summarydata(data)
    context = {
        "data": data,
        "link": funcname,
        "totscan": summary[1],
        "totnotscan": summary[2],
        "totdata": summary[0],
        "percent": f"{summary[3]:.3f}",
        "years": summary[4],
        "menu": getmenu(),
    }
    
    return render(request=request, template_name='alihmedia_inactive/irigasi.html', context=context)

def air_baku(request):
    funcname = sys._getframe().f_code.co_name
    data = getdata(method=request.method, parquery=request.GET.get("search"))
    summary = summarydata(data)
    context = {
        "data": data,
        "link": funcname,
        "totscan": summary[1],
        "totnotscan": summary[2],
        "totdata": summary[0],
        "percent": f"{summary[3]:.3f}",
        "years": summary[4],
        "menu": getmenu(),
    }
    return render(request=request, template_name='alihmedia_inactive/irigasi.html', context=context)

def sungai(request):
    funcname = sys._getframe().f_code.co_name
    data = getdata(method=request.method, parquery=request.GET.get("search"))
    summary = summarydata(data)
    context = {
        "data": data,
        "link": funcname,
        "totscan": summary[1],
        "totnotscan": summary[2],
        "totdata": summary[0],
        "percent": f"{summary[3]:.3f}",
        "years": summary[4],
        "menu": getmenu(),
    }
    return render(request=request, template_name='alihmedia_inactive/irigasi.html', context=context)

def pantai(request):
    funcname = sys._getframe().f_code.co_name
    data = getdata(method=request.method, parquery=request.GET.get("search"))
    summary = summarydata(data)
    context = {
        "data": data,
        "link": funcname,
        "totscan": summary[1],
        "totnotscan": summary[2],
        "totdata": summary[0],
        "percent": f"{summary[3]:.3f}",
        "years": summary[4],
        "menu": getmenu(),
    }
    return render(request=request, template_name='alihmedia_inactive/irigasi.html', context=context)

def keuangan(request):
    funcname = sys._getframe().f_code.co_name
    data = getdata(method=request.method, parquery=request.GET.get("search"))
    summary = summarydata(data)
    context = {
        "data": data,
        "link": funcname,
        "totscan": summary[1],
        "totnotscan": summary[2],
        "totdata": summary[0],
        "percent": f"{summary[3]:.3f}",
        "years": summary[4],
        "menu": getmenu(),
    }
    return render(request=request, template_name='alihmedia_inactive/irigasi.html', context=context)

def pdfdownload(request, link, doc_id):
    doc = Doc.objects.get(id=doc_id)
    path = os.path.join(settings.PDF_LOCATION, __package__.split('.')[0], link, str(doc.bundle.box_number), str(doc.doc_number) + ".pdf")
    if exists(path):
        filename = f"{__package__.split('.')[0]}_{link}_{doc.bundle.box_number}_{doc.doc_number}.pdf"
        with open(path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline;filename={filename}.pdf'
            return response
    raise Http404    

def statistics_old(request):
    deps = Department.objects.all()
    depnamelist = []
    depvaluelist = []
    colorlist = []
    foundall = 0
    notfoundall = 0
    for d in deps:
        docs = Doc.objects.filter(bundle__department_id__exact=d.id)
        found = 0
        notfound = 0
        total = len(docs)
        for ke, doc in enumerate(docs):
            path = os.path.join(settings.PDF_LOCATION, __package__.split('.')[0], d.link, str(doc.bundle.box_number), str(doc.doc_number) + ".pdf")
            if exists(path):
                foundall += 1
                found += 1
            else:
                notfoundall += 1
                notfound += 1
        depnamelist.append(" | ".join([d.name, "Sudah"]))
        depnamelist.append(" | ".join([d.name, "Belum"]))
        depvaluelist.append(found)
        depvaluelist.append(notfound)
        colorlist.append("rgba(112, 185, 239, 1)")
        colorlist.append("rgba(244, 204, 204, 1)")
        total = foundall + notfoundall
        procfound = foundall / total * 100
        procnotfound = notfoundall / total * 100
    context = {
        "menu": getmenu(),
        "depnamelist": depnamelist,
        "depvaluelist": depvaluelist,
        "colorlist": colorlist,
        "foundall": str(foundall),
        "notfoundall": str(notfoundall),
        "procfound":f"{procfound:.3f}",
        "procnotfound":f"{procnotfound:.3f}",
    }

    return render(request=request, template_name='alihmedia_inactive/statistics.html', context=context)



def statistics(request):
    deps = Department.objects.all()
    depnamelist = []
    depvaluelist = []
    colorlist = []
    foundall = 0
    notfoundall = 0
    for d in deps:
        foundlist = [os.path.join(root, file) for root, dirs, files in os.walk(os.path.join(settings.PDF_LOCATION, __package__.split('.')[0], d.link)) for file in files if file.endswith(".pdf")]
        found = len(foundlist)
        foundall += found
        docs = Doc.objects.filter(bundle__department_id__exact=d.id)
        notfound = len(docs) - found
        notfoundall += notfound
        depnamelist.append(" | ".join([d.name, "Sudah"]))
        depnamelist.append(" | ".join([d.name, "Belum"]))
        depvaluelist.append(found)
        depvaluelist.append(notfound)
        colorlist.append("rgba(112, 185, 239, 1)")
        colorlist.append("rgba(244, 204, 204, 1)")
        total = foundall + notfoundall
        procfound = foundall / total * 100
        procnotfound = notfoundall / total * 100
    
    fileinfolist = []
    allfilelist = [os.path.join(root, file) for root, dirs, files in os.walk(os.path.join(settings.PDF_LOCATION, __package__.split('.')[0])) for file in files if file.endswith(".pdf")]
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
    # groupdates = {}
    # docdate = []
    # docscan = []
    # doccolor = []
    # for item in fileinfolist:
    #     groupdates.setdefault(item['date'], []).append(item)

    # for key, value in groupdates.items():
    #     docdate.append(key)
    #     docscan.append(len(value))
    #     doccolor.append("rgba(112, 185, 239, 1)")

    context = {
        "menu": getmenu(),
        "depnamelist": depnamelist,
        "depvaluelist": depvaluelist,
        "colorlist": colorlist,
        "foundall": str(foundall),
        "notfoundall": str(notfoundall),
        "procfound":f"{procfound:.3f}",
        "procnotfound":f"{procnotfound:.3f}",
        "docdate": docdate,
        "docscan": docscan,
        "doccolor": doccolor,
    }

    return render(request=request, template_name='alihmedia_inactive/statistics.html', context=context)



def tes1(request):
    fileinfolist = []
    allfilelist = [os.path.join(root, file) for root, dirs, files in os.walk(os.path.join(settings.PDF_LOCATION, __package__.split('.')[0])) for file in files if file.endswith(".pdf")]
    for filepath in allfilelist:
        infotime = os.path.getmtime(filepath)
        infodate = datetime.fromtimestamp(infotime).strftime('%d-%m-%Y')
        mdict = {
            "file": filepath,
            "date": infodate,
            "pages": fitz.open(filepath).page_count
        }
        fileinfolist.append(mdict)

    d = {}
    
    for item in fileinfolist:
        d.setdefault(item['date'], []).append(item)
    

    return HttpResponse( d.values())

def tes2(request):
    l = []
    foundlist = [os.path.join(root, file) for root, dirs, files in os.walk(os.path.join(settings.PDF_LOCATION, __package__.split('.')[0], "irigasi")) for file in files if file.endswith(".pdf")]
    for filepath in foundlist:
        infotime = os.path.getmtime(filepath)
        infodate = datetime.fromtimestamp(infotime).strftime('%d-%m-%Y')
        # infodate = time.ctime(infotime)
        l.append(filepath + " | " + infodate)

    return HttpResponse("<br/>".join(l))
