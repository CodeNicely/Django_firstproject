from django.http import HttpResponse, JsonResponse, request
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from student.models import user_data


@csrf_exempt
def register(request):
    if request.method == 'GET':
        print ('inside if')
        return render(request, "register.html")

    if request.method == 'POST':
        print ('inside post method')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        user_data.objects.create(
            username=name,
            mobile=mobile,
            password=password
        )
        json = {'result': True}
        return JsonResponse(json)


def login(request):
    if request.method == 'GET':
        print ('inside login')
        return render(request, "login.html")

    if request.method == 'POST':
        print ('inside post method')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        user = user_data.objects.get(mobile=int(mobile))
        print user
        if user.password == password:
            return JsonResponse(user)


