# from django.shortcuts import render
# from rest_framework import generics, permissions
# from rest_framework.response import Response


# # class ProfileView(generics.RetrieveUpdateAPIView):
# #     serializer_class = ProfileSerializer
# #     permission_classes = [permissions.IsAuthenticated]

# #     def get_object(self):
# #         profile, created = Profile.objects.get_or_create(user=self.request.user)
# #         return profile
# from rest_framework import generics, permissions
# from .models import Profile
# from .serializers import ProfileSerializer

# class ProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         # This will create profile automatically if it doesn't exist
#         profile, created = Profile.objects.get_or_create(user=self.request.user)
#         return profile
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
from accounts.models import User

# Your existing view (rename to MyProfileView or keep as ProfileView)
class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PUT/PATCH /api/profiles/me/ – logged in user's profile + posts"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

# New public view to see any user's profile + posts
class UserProfileView(generics.RetrieveAPIView):
    """GET /api/profiles/user/<id>/ – any user's profile + posts (public)"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        profile, created = Profile.objects.get_or_create(user=user)
        return profile