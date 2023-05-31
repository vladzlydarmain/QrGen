from django.shortcuts import render

# Create your views here.
def show_editor(request):
    respones = render(request, "editor/editor.html")
    return respones