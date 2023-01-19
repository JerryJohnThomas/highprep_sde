from datetime import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# here i will be making my models for blog application 
class Category(models.Model):
    # this name will store the name of the category for a particular post 
    name = models.CharField(max_length=100);

    # i will be showing the name in the string format on the admin panel for our convienience
    def __str__(self):
        # say everything went fine 
        return self.name;


# now defining the model to store the information about each post 
class Post(models.Model):

    # defining the options that i will be using for status 
    available_options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    );

    # category here acts as the foreign key which will store to which category this post belongs to 
    # here we are using PROTECT because even the category is deleted from the database the post should not be deleted 
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1);
    title = models.CharField(max_length=250);
    excerpt = models.TextField(null=True);
    content = models.TextField();
    # this slug is nothing but instead of id we can also uniquely identify each of the post that is why we are using slug here 
    slug = models.SlugField(max_length=250, unique_for_date='published');
    published = models.DateTimeField(auto_now_add=True);
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts');
    status = models.CharField(max_length=100, choices=available_options, default='published');

    # defining the meta class for extra functionalities 
    class Meta:
        ordering  = ('-published', )

    def __str__(self):
        return self.title