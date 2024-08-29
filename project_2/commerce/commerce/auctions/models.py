from django.contrib.auth.models import AbstractUser
from django.db import models

Categories = [
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

# It is impossible to add a non-nullable field 'category' to listing without specifying a default. This is because the database needs something to populate existing rows.
#  Please select a fix: 
# ^
# this happens if you already make a migration and try to add a new table and insert a field with already existing data. It will conflict if some things are already existing.

class User(AbstractUser):
    # innate
    username =  models.CharField(unique=True, max_length=64)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    watchlist = [] # list of Objects.Listing || also this field is probably not necessary

    # acquired


class Listing(models.Model):
    # innate
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    image = models.CharField(max_length=3)
    category = models.CharField(max_length=64, choices=Categories)
    descripton = models.CharField(max_length=10000)

    # acquired
    lister = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self):
        return f"Item name: {self.name}"


class Bids(models.Model):
    # innate
    price = models.IntegerField(default=0)# why this too?

    # acquired
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE) # because listing has a field that refers to AbstractUser Therefore null field occurs
    bidder = models.ForeignKey(User, on_delete=models.CASCADE) # because its a foreign key referring to AbstractUser

    def __str__(self):
        return f"{self.bidder})"

class Comments(models.Model):
    # innate
    comment = models.TextField(default='', blank=False)
    date = models.DateField()
    time = models.TimeField()
    
    
    # acquired
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self):
        return f"Comment from:{self.commenter} on listing:{self.listing})"

class Watchlist(models.Model):
    # innate

    # acquired
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)

    def __str__(self):
        return f"Watchlist item from:{self.user}. Item being watched:{self.listing})"
