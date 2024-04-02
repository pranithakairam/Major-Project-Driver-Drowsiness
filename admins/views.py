from django.shortcuts import render, HttpResponse
from django.contrib import messages
from users.models import DriverRegistrationModel,FattigueInfoModel


# Create your views here.

def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'admins/AdminHome.html')
        elif usrid == 'Admin' and pswd == 'Admin':
            return render(request, 'admins/AdminHome.html')
        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def AdminHome(request):
    return render(request, 'admins/AdminHome.html')


def ViewRegisteredAutoists(request):
    data = DriverRegistrationModel.objects.all()
    return render(request, 'admins/ViewRegisterAutoists.html', {'data': data})


def AdminActivaAutoists(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        DriverRegistrationModel.objects.filter(id=id).update(status=status)
        data = DriverRegistrationModel.objects.all()
        return render(request, 'admins/ViewRegisterAutoists.html', {'data': data})


def AdminDeleteAutoists(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        DriverRegistrationModel.objects.filter(id=id).delete()
        data = DriverRegistrationModel.objects.all()
        return render(request, 'admins/ViewRegisterAutoists.html', {'data': data})


def AdminViewFatigueHistory(request):
    qs = FattigueInfoModel.objects.all()
    return render(request, 'admins/ViewAutoistsHistory.html', {'data': qs})

