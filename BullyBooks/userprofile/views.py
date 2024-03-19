from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Userprofile
# from django.shortcuts import redirect

# Create your views here.
def seller_detail(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'userprofile/seller_detail.html', {
        'user': user
    })

def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            userprofile = Userprofile.objects.create(user=user)
            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'userprofile/signup.html', {
        'form': form
    })

def my_account(request):
    return render(request, 'userprofile/myaccount.html')