from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from django.core.paginator import Paginator
from .models import Follower, FollowerForm


from .models import User, Post, Like, Follower


def index(request):
        if request.method == "POST":
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse("register"))
            
            content = request.POST["content"]
            print(content)
            Post.objects.create(post_content=content, user_id=request.user)
            return HttpResponseRedirect(reverse("index"))
        else:
            posts_list = Post.objects.all().order_by('-post_time')
            paginator = Paginator(posts_list, 10)
            try:
                page = request.GET.get('page', '1')
            except:
                page = 1
            try:
                posts = paginator.page(page)
            except:
                posts = paginator.page(paginator.num_pages)

            if request.user.is_authenticated:
                username = User.objects.get(username=request.user).username
                likes_dict = {}
                if not posts:
                    return render(request, "network/index.html", {
                    "username":username,
                })
                for post in posts:
                    likes = int(Like.objects.filter(post_id=post.id).count())
                    likes_minus = int(Like.objects.filter(post_id=post.id).count()) -1
                    if likes_minus <= 0:
                        likes_minus = 0
                    likes_plus = int(Like.objects.filter(post_id=post.id).count()) +1
                    likers = Like.objects.filter(post_id=post.id)
                    likers_list = []
                    for liker in likers:
                        likers_list.append(liker.liker_id)
                    post_id = post.id
                    likes_dict[post_id] = (likes, likers_list, likes_minus, likes_plus)

                return render(request, "network/index.html", {
                    "posts":posts,
                    "likes":likes,
                    "username":username,
                    "likes_dict":likes_dict
                })
            else:
                posts_list = Post.objects.all().order_by('-post_time')
                paginator = Paginator(posts_list, 10)
                try:
                    page = request.GET.get('page', '1')
                except:
                    page = 1
                try:
                    posts = paginator.page(page)
                except:
                    posts = paginator.page(paginator.num_pages)
 
                likes_dict = {}
                for post in posts:
                    likes = Like.objects.filter(post_id=post.id).count()
                    likes_minus = int(Like.objects.filter(post_id=post.id).count()) -1
                    if likes_minus <= 0:
                        likes_minus = 0
                    likes_plus = int(Like.objects.filter(post_id=post.id).count()) +1
                    likers = Like.objects.filter(post_id=post.id)
                    likers_list = []
                    for liker in likers:
                        likers_list.append(liker.liker_id)
                    post_id = post.id
                    likes_dict[post_id] = (likes, likers_list, likes_minus, likes_plus)

                return render(request, "network/index.html", {
                    "posts":posts,
                    "likes":likes,
                    "likes_dict":likes_dict
                })
            
@csrf_exempt
def posting(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post = data.get("post_id", "")
        post_id = Post.objects.get(id=post)
        liker = data.get("liker_id", "")
        liker_id = User.objects.get(username=liker)
        like = Like.objects.create(post_id=post_id, liker_id=liker_id)

        like.save()
        return JsonResponse({"message": "Like added"})

    if request.method == "DELETE":
        data = json.loads(request.body)
        post = data.get("post_id", "")
        post_id = Post.objects.get(id=post)
        liker = data.get("liker_id", "")
        liker_id = User.objects.get(username=liker)
        like = Like.objects.get(post_id=post_id, liker_id=liker_id)

        like.delete()
        return JsonResponse({"message": "Like deleted"})

    if request.method == "PUT":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        data = json.loads(request.body)
        print(data)
        post_id = data.get("post_id", "")
        print(post_id)
        post = Post.objects.get(id=post_id)
        print(post)


        content = data.get("content", "")
        if content:
            if request.user != post.user_id:
                return JsonResponse({"error": "Can only edit your own posts"})
            post.post_content = content
        post.save()
        #like.save()
        return JsonResponse({"message": "Post edited successfully"})
    if request.method != "POST" and request.method != "PUT" and request.method != "DELETE":
        return JsonResponse({"error": "PUT, POST or DELETE request required."}, status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
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

def profile_view(request, username):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("register"))

        if "UnFollow" in request.POST:
            follow_initiator_id = User.objects.get(username=request.user)
            print(follow_initiator_id)
            follow_reciever_id = User.objects.get(username=username)
            print(follow_reciever_id)
            Follower.objects.get(follow_initiator=follow_initiator_id, follow_reciever=follow_reciever_id).delete()
            return HttpResponseRedirect(reverse("profile", args=(username,)))
        
        if "Follow" in request.POST:
            follow_initiator_id = User.objects.get(username=request.user)
            print(follow_initiator_id)
            follow_reciever_id = User.objects.get(username=username)
            print(follow_reciever_id)
            Follower.objects.create(follow_initiator=follow_initiator_id, follow_reciever=follow_reciever_id)
            return HttpResponseRedirect(reverse("profile", args=(username,)))
        else:
            content = request.POST["content"]
            print(content)
            Post.objects.create(post_content=content, user_id=request.user)
            return HttpResponseRedirect(reverse("profile", args=(username,)))
    else:
        if request.user.is_authenticated:
            user = request.user
            userstring = str(request.user)
            whos_page = username
            page_id = User.objects.get(username=whos_page).id
            posts_list = Post.objects.filter(user_id=page_id).order_by('-post_time')
            paginator = Paginator(posts_list, 10)
            try:
                page = request.GET.get('page', '1')
            except:
                page = 1
            try:
                posts = paginator.page(page)
            except:
                posts = paginator.page(paginator.num_pages)
            likes_dict = {}
            if not posts:
                return render(request, "network/profile.html", {
                "username":username,
            })
            for post in posts:
                likes = Like.objects.filter(post_id=post.id).count()
                likes_minus = int(Like.objects.filter(post_id=post.id).count()) -1
                if likes_minus <= 0:
                    likes_minus = 0
                likes_plus = int(Like.objects.filter(post_id=post.id).count()) +1
                likers = Like.objects.filter(post_id=post.id)
                likers_list = []
                for liker in likers:
                    likers_list.append(liker.liker_id)
                post_id = post.id
                likes_dict[post_id] = (likes, likers_list, likes_minus, likes_plus)

            followers = Follower.objects.filter(follow_reciever = page_id)
            follow_list = []
            for follower in followers:
                follow_list.append(follower.follow_initiator)
            follower_count = Follower.objects.filter(follow_reciever = page_id).count
            following_count = Follower.objects.filter(follow_initiator = page_id).count

            return render(request, "network/profile.html",{
                "whos_page":whos_page,
                "likes":likes,
                "likes_dict":likes_dict,
                "user":user,
                "userstring":userstring,
                "username":user,
                "posts":posts,
                "following_count":following_count,
                "follower_count":follower_count,
                "follow_list":follow_list
            })
        else:
            whos_page = username
            page_id = User.objects.get(username=whos_page).id
            posts_list = Post.objects.filter(user_id=page_id).order_by('-post_time')
            paginator = Paginator(posts_list, 10)
            try:
                page = request.GET.get('page', '1')
            except:
                page = 1
            try:
                posts = paginator.page(page)
            except:
                posts = paginator.page(paginator.num_pages)
            likes_dict = {}
            for post in posts:
                likes = int(Like.objects.filter(post_id=post.id).count())
                likes_minus = int(Like.objects.filter(post_id=post.id).count()) -1
                if likes_minus <= 0:
                    likes_minus = 0
                likes_plus = int(Like.objects.filter(post_id=post.id).count()) +1
                likers = Like.objects.filter(post_id=post.id)
                likers_list = []
                for liker in likers:
                    likers_list.append(liker.liker_id)
                post_id = post.id
                likes_dict[post_id] = (likes, likers_list, likes_minus, likes_plus)


            followers = Follower.objects.filter(follow_reciever = page_id)
            print(followers)
            follower_count = Follower.objects.filter(follow_reciever = page_id).count
            following_count = Follower.objects.filter(follow_initiator = page_id).count


            return render(request, "network/profile.html",{
                "whos_page":whos_page,
                "posts":posts,
                "following_count":following_count,
                "follower_count":follower_count,
                "followers":followers,
                "likes":likes,
                "likes_dict":likes_dict
            })


def following(request): 
    username = User.objects.get(username=request.user).username
    followed = Follower.objects.filter(follow_initiator=request.user)
    if str(followed) == "<QuerySet []>":
        return render(request, "network/following.html", {
        "username":username,
    })
    for i in followed:
        posts_list = Post.objects.filter(user_id=i.follow_reciever).order_by('-post_time')
    paginator = Paginator(posts_list, 10)
    try:
        page = request.GET.get('page', '1')
    except:
        page = 1
    try:
        posts = paginator.page(page)
    except:
        posts = paginator.page(paginator.num_pages)
    likes_dict = {}
    if not posts:
        return render(request, "network/following.html", {
        "username":username,
        })
    for post in posts:
        likes = Like.objects.filter(post_id=post.id).count()
        likes_minus = int(Like.objects.filter(post_id=post.id).count()) -1
        if likes_minus <= 0:
            likes_minus = 0
        likes_plus = int(Like.objects.filter(post_id=post.id).count()) +1
        likers = Like.objects.filter(post_id=post.id)
        likers_list = []
        for liker in likers:
            likers_list.append(liker.liker_id)
        post_id = post.id
        likes_dict[post_id] = (likes, likers_list, likes_minus, likes_plus)
    return render(request, "network/following.html", {
        "posts":posts,
        "likes":likes,
        "username":username,
        "likes_dict":likes_dict
    })

