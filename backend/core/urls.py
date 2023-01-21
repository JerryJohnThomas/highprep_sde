# this is the url file that will connect the other applications with this projects 
# all the endpoints will start going from this file itself 
# from django import views
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('inventory/', include('inventory_apis.urls', namespace = 'inventory_apis')),
    path('', include('login_apis.urls', namespace = 'login_apis')),
    path('api-token-auth/', views.obtain_auth_token),
    path('algo/', include('algo_apis.urls', namespace = 'algo_apis')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
