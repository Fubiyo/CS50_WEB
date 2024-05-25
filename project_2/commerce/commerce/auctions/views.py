from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bids, Comments

# django admin info / superuser
# user = qristaanterry
# password = Naatsirq96!

Categories = [
    ('', 'Please select a category'),
    ('electronics', 'Electronics'),
    ('fashion_accessories', 'Fashion & Accessories'),
    ('home_garden', 'Home & Garden'),
    ('sports_outdoors', 'Sports & Outdoors'),
    ('collectibles_art', 'Collectibles & Art'),
    ('toys_hobbies', 'Toys & Hobbies'),
    ('automotive', 'Automotive'),
    ('health_beauty', 'Health & Beauty'),
    ('books_movies_music', 'Books, Movies & Music'),
    ('computers_software', 'Computers & Software'),
    ('jewelry_watches', 'Jewelry & Watches'),
    ('baby_kids', 'Baby & Kids'),
    ('pet_supplies', 'Pet Supplies'),
    ('business_industrial', 'Business & Industrial'),
    ('crafts_diy', 'Crafts & DIY'),
]   # this list has to be a tuple, learn why.

class Create_Listing(forms.Form):
    name = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'name'
        }))
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'max': 1000,
            'placeholder': 'price'
        }))
    image = forms.CharField(
        max_length=3,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'IMG?'
        })) # 3 letter word placeholder for now cause idk how to image
    description = forms.CharField(
        max_length=10000,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'describe your item:'
        }))
    category = forms.ChoiceField(
        choices=Categories,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select'
        }))

def success(request):
    return render(request, "auctions/success.html")

def fail(request):
    return render(request, "auctions/fail.html")

def index(request):

   # create object which is a list of all active listings
    active_listings = Listing.objects.all()

    if active_listings:

        print(active_listings)
        print(type(active_listings))
    else:
        return HttpResponseRedirect(reverse("auctions:fail"), {
            "fail": "active listings didnt exist or soemthing idk"
        })
    
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
    })

def categories(request):
    if request.method == "POST":
        return render(request, "auctions/categories.html")
    else:
        return render(request, "auctions/categories.html")

def watchlist(request):
    if request.method == "POST":
        return render(request, "auctions/watchlist.html")
    else:
        return render(request, "auctions/watchlist.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        listing_form = Create_Listing(request.POST)
        if listing_form.is_valid():
            
            # create an instance of listing model
            listing = Listing()

            # clean form data
            listing_form_cleaned = listing_form.cleaned_data # clean the form data

            # validation check for category field from form submission
            if listing_form_cleaned["category"] in Categories:
                pass
            else:
                return HttpResponseRedirect(reverse("auctions:fail"), {
                "fail": "submitted category was not in category"
            })
        
            # access cleand data as easy to read variables || name, price, image, description, category
            name = listing_form_cleaned["name"]
            price = listing_form_cleaned["price"]
            image = listing_form_cleaned["image"]
            description = listing_form_cleaned["description"]
            category = listing_form_cleaned["category"]
            
            # populate model with cleaned form data
            listing.name = name
            listing.price = price
            listing.image = image
            listing.description = description
            listing.category = category
            listing.lister = User.objects.get(username=request.user)

            # save populated model to database
            listing.save()


            # operation successful therefore return desired route
            return HttpResponseRedirect(reverse("auctions:success"), {
                "name": name,
                "price": price
            })
        
        else: # assuming the form was submitted somehow but data is not valid therefore object will not be created
             return render(request, "auctions/create_listing.html", {
            "create_listing_form": Create_Listing,
            "categories": Categories
        })
        
    else:
        # render create_listing.html template
        return render(request, "auctions/create_listing.html", {
            "create_listing_form": Create_Listing,
            "categories": Categories
        })
    
def listings(request, id):
    listing = Listing.objects.get(id=id)
    if listing:
        print(listing)
    else:
        return render(request, "auctions/fail.html")

    return render(request, "auctions/success.html", {
        "success": listing
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password) # positional arguments?
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
