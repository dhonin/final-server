# # from rest_framework import serializers
# # from .models import Profile

# # class ProfileSerializer(serializers.ModelSerializer):
# #     email = serializers.EmailField(source='user.email', read_only=True)
# #     role = serializers.CharField(source='user.role', read_only=True)
# #     full_name = serializers.SerializerMethodField()

# #     class Meta:
# #         model = Profile
# #         fields = [
# #             'id', 'email', 'role', 'full_name',
# #             'phone', 'address', 'bio', 'profile_picture',
# #             'linkedin_url', 'github_url', 'portfolio_url',
# #             'skills', 'experience', 'education', 'resume',
# #             'company_name', 'company_website', 'designation',
# #             'created_at', 'updated_at'
# #         ]
# #         read_only_fields = ['id', 'email', 'role', 'full_name', 'created_at', 'updated_at']

# #     def get_full_name(self, obj):
# #         return f"{obj.user.first_name} {obj.user.last_name}".strip()

# #     def create(self, validated_data):
# #         user = self.context['request'].user
# #         profile, _ = Profile.objects.get_or_create(user=user)
# #         for attr, value in validated_data.items():
# #             setattr(profile, attr, value)
# #         profile.save()
# #         return profile
# # from rest_framework import serializers
# # from .models import Profile

# # class ProfileSerializer(serializers.ModelSerializer):
# #     email = serializers.EmailField(source='user.email', read_only=True)
# #     role = serializers.CharField(source='user.role', read_only=True)
# #     full_name = serializers.SerializerMethodField()

# #     class Meta:
# #         model = Profile
# #         fields = [
# #             'id', 'email', 'role', 'full_name',
# #             'phone', 'address', 'bio', 'profile_picture',
# #             'linkedin_url', 'github_url', 'portfolio_url',
# #             'skills', 'experience', 'education', 'resume',
# #             'company_name', 'company_website', 'designation',
# #             'created_at', 'updated_at'
# #         ]
# #         read_only_fields = ['id', 'email', 'role', 'full_name', 'created_at', 'updated_at']

# #     def get_full_name(self, obj):
# #         return f"{obj.user.first_name} {obj.user.last_name}".strip()

# #     def create(self, validated_data):
# #         user = self.context['request'].user
# #         profile, _ = Profile.objects.get_or_create(user=user)
# #         for attr, value in validated_data.items():
# #             setattr(profile, attr, value)
# #         profile.save()
# #         return profile
# # from rest_framework import serializers
# # from .models import Profile

# # class ProfileSerializer(serializers.ModelSerializer):
# #     email = serializers.EmailField(source='user.email', read_only=True)
# #     role = serializers.CharField(source='user.role', read_only=True)
# #     full_name = serializers.SerializerMethodField()

# #     class Meta:
# #         model = Profile
# #         fields = [
# #             'id', 'email', 'role', 'full_name',
# #             'phone', 'address', 'bio', 'profile_picture',
# #             'linkedin_url', 'github_url', 'portfolio_url',
# #             'skills', 'experience', 'education', 'resume',
# #             'company_name', 'company_website', 'designation',
# #             'created_at', 'updated_at'
# #         ]
# #         read_only_fields = ['id', 'email', 'role', 'full_name', 'created_at', 'updated_at']

# #     def get_full_name(self, obj):
# #         return f"{obj.user.first_name} {obj.user.last_name}".strip()
# from rest_framework import serializers
# from .models import Profile

# class ProfileSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='user.email', read_only=True)
#     role = serializers.CharField(source='user.role', read_only=True)
#     full_name = serializers.SerializerMethodField()
#     posts = serializers.SerializerMethodField()
#     posts_count=serializers.SerializerMethodField()

#     class Meta:
#         model = Profile
#         fields = [
#             'id', 'email', 'role', 'full_name',
#             'phone', 'address', 'bio', 'profile_picture',
#             'linkedin_url', 'github_url', 'portfolio_url',
#             # Seeker fields
#             'skills', 'experience', 'education', 'resume',
#             # HR fields
#             'company_name', 'company_website', 'designation',
#             'created_at', 'updated_at'
#             'posts','posts_count'
#         ]
#         read_only_fields = ['id', 'email', 'role', 'full_name', 'created_at', 'updated_at']

#     def get_full_name(self, obj):
#         return f"{obj.user.first_name or ''} {obj.user.last_name or ''}".strip()

#     def validate(self, data):
#         user_role = self.context['request'].user.role
        
#         if user_role == 'seeker':
#             # HR fields should be empty for seekers
#             hr_fields = ['company_name', 'company_website', 'designation']
#             for field in hr_fields:
#                 if data.get(field):
#                     raise serializers.ValidationError({field: "This field is only for HR users."})
                    
#         elif user_role == 'hr':
#             # Seeker fields should be empty for HR
#             seeker_fields = ['skills', 'experience', 'education', 'resume']
#             for field in seeker_fields:
#                 if data.get(field):
#                     raise serializers.ValidationError({field: "This field is only for Job Seeker users."})

#         return data
from rest_framework import serializers
from .models import Profile
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import serializers
from accounts.models import User

# class ProfileSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='user.email', read_only=True)
#     role = serializers.CharField(source='user.role', read_only=True)
#     full_name = serializers.SerializerMethodField()
    
#     # Posts integration
#     posts = serializers.SerializerMethodField()
#     posts_count = serializers.SerializerMethodField()
#     followers_count = serializers.SerializerMethodField()
#     following_count = serializers.SerializerMethodField()


#     class Meta:
#         model = Profile
#         fields = [
#             'id', 'email', 'role', 'full_name',
#             'phone', 'address', 'bio', 'profile_picture',
#             'linkedin_url', 'github_url', 'portfolio_url',
#             # Seeker fields
#             'skills', 'experience', 'education', 'resume',
#             # HR fields
#             'company_name', 'company_website', 'designation',
#             'created_at', 'updated_at',
#             'posts', 'posts_count',
#             'followers_count', 'following_count',
#         ]
#         read_only_fields = ['id', 'email', 'role', 'full_name', 'created_at', 'updated_at']

#     def get_full_name(self, obj):
#         first = obj.user.first_name or ''
#         last = obj.user.last_name or ''
#         return f"{first} {last}".strip() or obj.user.email

#     def get_posts(self, obj):
#         # Return all posts by this user, newest first
#         posts = Post.objects.filter(author=obj.user).order_by('-created_at')
#         request = self.context.get('request')
#         return PostSerializer(posts, many=True, context={'request': request}).data

#     def get_posts_count(self, obj):
#         return Post.objects.filter(author=obj.user).count()

#     def validate(self, data):
#         user_role = self.context['request'].user.role

#         if user_role == 'seeker':
#             # HR fields should be empty for seekers
#             hr_fields = ['company_name', 'company_website', 'designation']
#             for field in hr_fields:
#                 if data.get(field):
#                     raise serializers.ValidationError({field: "This field is only for HR users."})
#         elif user_role == 'hr':
#             # Seeker fields should be empty for HR
#             seeker_fields = ['skills', 'experience', 'education', 'resume']
#             for field in seeker_fields:
#                 if data.get(field):
#                     raise serializers.ValidationError({field: "This field is only for Job Seeker users."})
#         return data
#     def get_followers_count(self, obj):
#         return obj.user.followers_set.count()   # from network app

#     def get_following_count(self, obj):
#         return obj.user.following_set.count()
class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    full_name = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    # Override skills to accept either list or comma-separated string
    skills = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        help_text="List of skills (e.g., ['Python', 'Django'])"
    )

    class Meta:
        model = Profile
        fields = [
            'id', 'email', 'role', 'full_name',
            'phone', 'address', 'bio', 'profile_picture',
            'linkedin_url', 'github_url', 'portfolio_url',
            'skills', 'experience', 'education', 'resume',
            'company_name', 'company_website', 'designation',
            'created_at', 'updated_at',
            'posts', 'posts_count',
            'followers_count', 'following_count'
        ]
        read_only_fields = ['id', 'email', 'role', 'full_name', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        first = obj.user.first_name or ''
        last = obj.user.last_name or ''
        return f"{first} {last}".strip() or obj.user.email

    def get_posts(self, obj):
        posts = Post.objects.filter(author=obj.user).order_by('-created_at')
        request = self.context.get('request')
        return PostSerializer(posts, many=True, context={'request': request}).data

    def get_posts_count(self, obj):
        return Post.objects.filter(author=obj.user).count()

    def get_followers_count(self, obj):
        return obj.user.followers_set.count()

    def get_following_count(self, obj):
        return obj.user.following_set.count()

    def validate(self, data):
        user_role = self.context['request'].user.role

        if user_role == 'seeker':
            hr_fields = ['company_name', 'company_website', 'designation']
            for field in hr_fields:
                if data.get(field):
                    raise serializers.ValidationError({field: "This field is only for HR users."})
        elif user_role == 'hr':
            seeker_fields = ['skills', 'experience', 'education', 'resume']
            for field in seeker_fields:
                if data.get(field):
                    raise serializers.ValidationError({field: "This field is only for Job Seeker users."})
        return data

    def to_internal_value(self, data):
        """Convert a comma-separated string to a list if needed"""
        skills_data = data.get('skills')
        if isinstance(skills_data, str):
            # Convert "Python, Django" -> ["Python", "Django"]
            skills_list = [s.strip() for s in skills_data.split(',') if s.strip()]
            data = data.copy()
            data['skills'] = skills_list
        return super().to_internal_value(data)

class UserBasicSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'profile_picture', 'bio']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.email

    def get_profile_picture(self, obj):
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            # If profile_picture is an ImageField, return its URL
            return obj.profile.profile_picture.url if obj.profile.profile_picture else None
        return None

    def get_bio(self, obj):
        if hasattr(obj, 'profile') and obj.profile.bio:
            return obj.profile.bio[:120]   # short preview for cards
        return ""
