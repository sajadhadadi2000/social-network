from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
import json

from .models import User, Post
from .forms import NewPost

def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("post", kwargs={"page" : "allpost"}))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def createpost(request):
    
    if request.method == 'POST':
        form = NewPost(request.POST)
        
        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title'] 
            body = form.cleaned_data['body']

            newpost = Post(user=user, title=title, body=body)
            newpost.save()
            
            return HttpResponseRedirect(reverse("post" , kwargs={"page" : "allpost"}))
        else:
            form = NewPost()
            return render(request, "network/newpost.html", {"form" : form})

    else:
        form = NewPost()
        return render(request, "network/newpost.html", {"form" : form})

def post(request, page):
    if page == "allpost":
        posts = Post.objects.all().order_by("-time")
    elif page == "following":
        user = User.objects.get(username=request.user)
        following = user.following.all()
        posts = Post.objects.filter(user__in=following).order_by("-time")
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    post_per_page = paginator.get_page(page_number) 
    return render(request, "network/allpost.html", {"posts" : post_per_page})



def profile(request, username):
    user = get_object_or_404(User, username=request.user)
    profile_user = User.objects.get(username=username)
    posts = Post.objects.filter(user=profile_user).order_by("-time")
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    post_per_page = paginator.get_page(page_number) 
    if user.following.filter(id= profile_user.id).exists():
        button = "Unfollow"
    else:
        button = "Follow"

    profile = {
        "username" : profile_user,
        "npost" : posts.count(),
        "nfollower" : profile_user.follower.count(),
        "nfollowing" : profile_user.following.count(),
        "follow" : False if user == profile_user else True,
        "bfollow" : button
    }
    return render(request, "network/profile.html", {"posts" : post_per_page, "profile" : profile})

@csrf_exempt
def edit(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "post not found."}, status=404)

    if request.method == "POST":       
        data = json.loads(request.body)
        title = data["title"]
        body = data["body"]
    
        post.title = title
        post.body = body
        post.save()
        return JsonResponse({"massage": "Your post is edited"}, status=201)
    
    else:
        return JsonResponse(post.serialize(), safe=False)


@csrf_exempt
def follow(request, user_id):

    user = User.objects.get(username=request.user)
    following_user = User.objects.get(id=user_id)

    if user.following.filter(id=following_user.id).exists():
        user.following.remove(following_user)
        button = "Follow"
    else:
        user.following.add(following_user)
        button = "Unfollow"
    data = {'button' : button, 'nfollower' : following_user.follower.count()}   
    return JsonResponse(data, status=201)


@csrf_exempt
def like(request):

    if request.method == "PUT":
        user = User.objects.get(username=request.user)
        data = json.loads(request.body)
        post = get_object_or_404(Post, id=data["id"])

        if post.like.filter(id=user.id).exists():
            post.like.remove(user)
            buttonlike = False
        else:
            post.like.add(user)
            buttonlike = True
       
    return JsonResponse({"like": post.like.all().count(), "buttonlike": buttonlike}, status=201)

