from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from app.untils.verify_code import VerifyCode
# Create your views here.

def verify_code(request):
    verify_code = VerifyCode(width=147, height=45)
    request.session['v_code'] = verify_code.verify_code
    v_image = verify_code.verify_image
    f = BytesIO()
    v_image.save(f, 'jpeg')
    return HttpResponse(f.getvalue(), content_type='image/jpeg')