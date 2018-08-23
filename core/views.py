from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
# Create your views here.
def home_page(request):
    context = {
        "title":"Hello World!",
        "content":" Welcome to the homepage.",

    }
    if not request.user.is_authenticated:
    	return redirect("/login")
    if request.user.is_authenticated:
    	if request.user.has_scanned == False:
    		return redirect("account/scan")
    	else:
    		return render(request, "home_page.html", context)