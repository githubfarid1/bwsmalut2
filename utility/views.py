from django.shortcuts import render, redirect
from .forms import SearchQRCodeForm
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def qrcodesearch(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        url = request.POST['qrcode']
        # url = '/alihmedia_inactive/boxsearch/irigasi/2'
        return redirect(url)
    context = {}
    context['form'] = SearchQRCodeForm()
    # context['url'] = url
    return render(request,'utility/qrcodesearch.html', context=context)

