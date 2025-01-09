from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import User, Post


def index(request):
    return render(request, "network/profile_page.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


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
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
def all_posts(request):
    
    # # load all posts as an new object which will be a list of models.Post objects
    # post_list = posts = list(range(57))
    # # create a paginator object and populate it with list ob model objects, and set limit per page
    # paginator = Paginator(post_list,5)


    # # get page number the GET request which was made by clicking on a page number in the template
    # page_number = request.GET.get('page')
    # # determine which post to display based off of which page number was included with the request
    # posts_to_display = paginator.get_page(page_number)


    # return render(request, "network/all_posts.html", {
    #     "posts": posts,
    #     "posts_to_display": posts_to_display
    # })
    # ------------------------------------------------------------------------------------

    # retrieve all posts in database
    posts_list = Post.objects.all()
    
    # validate posts_list
    if posts_list:
        print(f"\nGood to go!\n")
    else:
        return render(request, "network/error.html", {
            "error": "error, no posts_list object"
        })

    # render all_posts template, pass in posts_list(query set) in as well
    return render(request, "network/all_posts.html", {
        "posts": posts_list
    }) 


def following(request):
    pass

def new_post(request):
    return render(request, "network/new_post.html")

def profile_page(request):
    pass

@login_required
@csrf_exempt
def create_post(request):
    
    if request.method == "POST":
        
        # parse form data
        poster = request.user
        description = request.POST.get("description")

        # validate post data attempt
        if not description:
            return render(request, "network/test_create_post.html", {
                "result": "Creating post was unsuccessful because input is blank try again"
            })

        # attempt to create object and save
        try:  
            post = Post(poster=poster,description=description)
            post.save()
            retrieve = Post.objects.filter(poster=request.user)

            return render(request, "network/test_create_post.html", {
                "result": "Route path is accessable",
                "post": post, # current post that was made
                "retrieve": retrieve # all posts from user
            })
        except IntegrityError as e:
            return render(request, "network/test_create_post.html", {
                "result": e
            })
 
    else:
        return HttpResponseRedirect(reverse("network:index"))

@csrf_exempt  
def likes(request):

    if request.method == "PUT":
        
        id = request.user.id

        print(f"visited! {id}\n")

        return JsonResponse({
            "message": "Route is good to go!",
            "id": id
        })
    else:
        print("not good bro")
        return HttpResponseRedirect(reverse("network:index"))