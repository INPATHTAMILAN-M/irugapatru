from django.shortcuts import render
from .forms import Signup_Form, CustomAuthForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as user_logout
from django.conf import settings
from django.urls import reverse
import requests
from django.contrib import messages
from .models import User
from django.http import JsonResponse
# Create your views here.


# Create your views here.
def signup(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        data = dict()
        form = Signup_Form (request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = request.POST.get('email')
            user.save()

            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)


          
            if 'invited_game' in request.session:
                slug = request.session['invited_game']

                return redirect('/game/'+slug)
          
          
            

            data['valid'] = True
            return redirect('home')

        else:  
            return render(request,'registration/signup.html',{'form':form,})
    else:       
        form = Signup_Form()
    context = {
            'form':form,
           }
    return render(request,'registration/signup.html',context)


def customlogin(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    slug = None
    error = None
    if request.method == 'POST':
        
        form = CustomAuthForm(request.POST) 

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if 'invited_game' in request.session:
                    slug = request.session['invited_game']

                    return redirect('/game/'+slug)
                return redirect('home')


            else:
                error  = True
        else:
            error = True
        
                
    else:
        if 'invited_game' in request.session:
            slug = request.session['invited_game']
        form = CustomAuthForm()
     
    return render(request,'registration/login.html',{'form':form,'slug':slug,'error':error})



def logout(request):
    request.session['is_logout'] = True
    user_logout(request)
    return redirect('login')


#authentication
def google_login(request):
    redirect_uri = "%s://%s%s" % (
        "https", request.get_host(), reverse('google_login')
    )
    if('code' in request.GET):
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri': redirect_uri,
            'client_id': settings.GP_CLIENT_ID,
            'client_secret': settings.GP_CLIENT_SECRET
        }
        url = 'https://accounts.google.com/o/oauth2/token'
        response = requests.post(url, data=params)
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        access_token = response.json().get('access_token')
        response = requests.get(url, params={'access_token': access_token})
        user_data = response.json()
        
        email = user_data.get('email')
        if email:
            try:
                user= User.objects.get(email=str(email))
                slug = None
                if 'invited_game' in request.session:
                    slug = request.session['invited_game']
                    
                login(request, user)

                if slug:                  
                    return redirect('/game/'+slug)

                return redirect(reverse('home'))
            except:
               
                user = User.objects.create(first_name=user_data.get('name'), email=email,username=email)
                slug = None
                if 'invited_game' in request.session:
                    slug = request.session['invited_game']
                login(request, user)
                if slug:
                    request.session['invited_game'] = slug
                return redirect('add_gender')
                
        else:
            messages.error(
                request,
                'Unable to login with Gmail Please try again'
            )
        return redirect('/')
    else:
        url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
        scope = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email"
        ]
        scope = " ".join(scope)
        url = url % (settings.GP_CLIENT_ID, scope, redirect_uri)
        return redirect(url)
    


def add_gender(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            gender = request.POST.get('gender')
            user.gender = gender
            user.save()
            if 'invited_game' in request.session:
                slug = request.session['invited_game']
                return redirect('/game/'+slug)
            return redirect('home')
        else:
            return render(request,'registration/add_gender.html')
        

def terms_and_conditions(request):
    return render(request,'registration/terms.html')



def privacy_policy(request):
    return render(request,'registration/privacy.html')

            
    
        
     