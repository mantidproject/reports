from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")


def host_list(request):
    return render(request, "host_list.html")


def host(request, hostid):
    context = {"host": hostid}
    return render(request, "host.html", context)


def user_list(request):
    return render(request, "user_list.html")


def user(request, userid):
    context = {"uid": userid}
    return render(request, "user.html", context)
