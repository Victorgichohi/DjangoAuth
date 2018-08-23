from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
# Create your views here.
def home_page(request):
    # print(request.session.get("first_name", "Unknown"))
    # request.session['first_name']
    context = {
        "title":"Hello World!",
        "content":" Welcome to the homepage.",

    }
    if not request.user.is_authenticated:
    	return redirect("/login")
    return render(request, "home_page.html", context)