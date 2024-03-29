from django.shortcuts import render, HttpResponseRedirect
from App_Login.forms import CreateNewUser, EditProfile
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from App_Login.models import UserProfile, Follow
from django.contrib.auth.forms import AuthenticationForm
from App_Social.forms import PostForm
from django.contrib.auth.models import User

# SEND MAIL
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

# SIGNUP 
def sign_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            user = form.save()
            registered = True 
            user_profile = UserProfile(user=user) #models.
            user_profile.save()

            # mail
            # login(request, user)
            # subject = 'Greetings!!!'
            # message = f'Hi, {user.username}, Thank you for joining us.'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [user.email,]
            # send_mail(subject, message, email_from, recipient_list)

            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, 'App_Login/signup.html', context={'title':'Sign Up, Instagram', 'form': form})  



# LOGIN
def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Social:home'))
    return render(request, "App_Login/login.html", context={'title': 'Login', 'form': form})        
                 
@login_required
def edit_profile(request):
    current_user =  UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, "App_Login/profile.html", context={'title': 'Edit Profile | Social', 'form': form})        


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("App_Login:login"))
 
#  postform
@login_required
def profile(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('App_Social:home'))
    return render(request, 'App_Login/user.html', context={'title':'My Profile | Social', 'form': form})

# other Profile
@login_required
def user(request, username):
    user_other=User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user, following = user_other)
    if user_other == request.user:
        return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/user_other.html', context={'user_other':user_other, 'already_followed': already_followed})

# Follower
@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower = follower_user, following=following_user )
    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('App_Login:user', kwargs={'username': username}))

# unfollow
@login_required
def unfollow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower = follower_user, following=following_user )
    already_followed.delete()
    return HttpResponseRedirect(reverse('App_Login:user', kwargs={'username':username}))









