from django import forms
# creating a form  
class SearchQRCodeForm(forms.Form): 
    qrcode = forms.CharField(label="QR Code", max_length = 255, help_text = "Search QR Code") 
