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
# import fitz
 
# def get_size(file_path, unit='bytes'):
#     file_size = os.path.getsize(file_path)
#     exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
#     if unit not in exponents_map:
#         raise ValueError("Must select from \
#         ['bytes', 'kb', 'mb', 'gb']")
#     else:
#         size = file_size / 1024 ** exponents_map[unit]
#         return round(size, 3)

# def get_page_count(pdffile):
#     doc = fitz.open(pdffile)
#     return doc.page_count

# def generatecover(pdffile, coverfilename):
#     path = os.path.join(settings.COVER_LOCATION, coverfilename)
#     if not exists(path):
#         doc = fitz.open(pdffile)
#         page = doc.load_page(0)
#         pix = page.get_pixmap()
#         # output = "outfile.png"
#         pix.save(path)
#         doc.close()        
              
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


