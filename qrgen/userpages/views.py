from django.shortcuts import render

# Create your views here.
def show_profile(request):
    response = render(request, "userpages/profile.html")
    return response

def show_all_qr(request):
    response = render(request, "userpages/all-qr.html")
    return response
