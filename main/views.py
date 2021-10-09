from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from . import quantinsta

# Create your views here.
def landing(request):
    return render(request,'main/index.html',{})

def analytics_by_account(request,username):
    fig = quantinsta.comp_followers([username])
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)

    return render(request,'main/index.html',{'data':uri})