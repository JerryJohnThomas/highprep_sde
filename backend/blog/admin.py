from django.contrib import admin;
# importing all the models that we have defined till now for this purpose 
from .models import Post, Category; 

# Register your models here.
# here we have to register our models in order to show this on the admin panel for the superuser 
# for this purpose 
admin.site.register(Post);
admin.site.register(Category);
