"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from applications.views import RegisterFCMTokenView
from accounts.views import (
    AdminCandidatesListView,
    AdminHRsListView,
    AdminUserDeleteView,
    AdminUserStatusView,
    AdminUsersListView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/profiles/', include('profiles.urls')),  
    path('api/', include('posts.urls')),             
    path('api/', include('jobs.urls')),
    path('api/applications/', include('applications.urls')),
    path('api/network/', include('network.urls')),
    path('api/messaging/', include('messaging.urls')),
    path('api/alerts/', include('alerts.urls')),
    path('api/push/register/', RegisterFCMTokenView.as_view(),name='register-fcm'), 
    path('api/admin/users/', AdminUsersListView.as_view(), name='api-admin-users'),
    path('api/admin/hrs/', AdminHRsListView.as_view(), name='api-admin-hrs'),
    path('api/admin/candidates/', AdminCandidatesListView.as_view(), name='api-admin-candidates'),
    path('api/admin/users/<int:user_id>/', AdminUserDeleteView.as_view(), name='api-admin-user-delete'),
    path('api/admin/users/<int:user_id>/<str:action>/', AdminUserStatusView.as_view(), name='api-admin-user-status'),
]
