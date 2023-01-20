# this is the url file that will connect the other applications with this projects 
# all the endpoints will start going from this file itself 
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # this urls is for the admin panel in which we can go and create a super user for this
    # and after creating the super user we can manage the database for django project
    path("admin/", admin.site.urls),
    # here we have connected the blog and blog_api application using the urls.py 
    # path('', include('blog.urls', namespace = 'blog')),
    path('inventory/', include('inventory_apis.urls', namespace = 'inventory_apis')),
    path('', include('login_apis.urls', namespace = 'login_apis')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
