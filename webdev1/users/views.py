from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from proj_app.forms import SignUpForm, EditUserProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

# Create your views here.
def register(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            form.save()
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username = uname, password = upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request, 'users/login.html', {'form': fm})
    else:
         return HttpResponseRedirect('/profile/')
def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = EditUserProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                messages.success(request, 'Profile Updated!')
                fm.save()
        else:
            fm = EditUserProfileForm(instance = request.user)
        return render (request, 'users/profile.html', {'name': request.user, 'form':fm})
    else:
       return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def change_pass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data = request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password Change Successfully')
                return HttpResponseRedirect('/profile/')
        else:
          fm = PasswordChangeForm(user = request.user)
        return render(request, 'users/changepass.html', {'form': fm})
    else:
        return HttpResponseRedirect('/login/')


