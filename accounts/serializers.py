from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
import random
import string
import threading
from rest_framework import serializers
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from django.conf import settings
import dns.resolver
from django.core.cache import cache
        

User = get_user_model()
import dns.resolver

def is_real_email_domain(email):
    domain = email.split('@')[-1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except:
        return False

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=False)
    confirmPassword = serializers.CharField(write_only=True, required=False)
    firstName = serializers.CharField(write_only=True, required=False)
    lastName = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'firstName',
            'lastName',
            'role',
            'password',
            'confirm_password',
            'confirmPassword',
        )
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        attrs['first_name'] = attrs.pop('firstName', attrs.get('first_name', ''))
        attrs['last_name'] = attrs.pop('lastName', attrs.get('last_name', ''))

        confirm_password = attrs.get('confirm_password') or attrs.pop('confirmPassword', None)
        if attrs['password'] != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})

        if attrs.get('role') == 'candidate':
            attrs['role'] = 'seeker'

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        validated_data.pop('confirmPassword', None)
        user = User.objects.create_user(**validated_data)
        return user
    def validate_email(self, value):
        if not is_real_email_domain(value):
            raise serializers.ValidationError("Please use a valid email address (real domain).")
        return value 

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'role': 'candidate' if user.role == 'seeker' else user.role,
            }
        }

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    firstName = serializers.CharField(source='first_name', read_only=True)
    lastName = serializers.CharField(source='last_name', read_only=True)
    isSuspended = serializers.SerializerMethodField()
    jobsCount = serializers.SerializerMethodField()
    appliedJobs = serializers.SerializerMethodField()
    savedJobs = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'firstName',
            'lastName',
            'role',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
            'isSuspended',
            'jobsCount',
            'appliedJobs',
            'savedJobs',
        ]
        read_only_fields = fields

    def get_isSuspended(self, obj):
        return not obj.is_active

    def get_role(self, obj):
        if obj.is_superuser or obj.is_staff:
            return 'admin'
        return 'candidate' if obj.role == 'seeker' else obj.role

    def get_jobsCount(self, obj):
        return getattr(obj, 'posted_jobs', None).count() if hasattr(obj, 'posted_jobs') else 0

    def get_appliedJobs(self, obj):
        from applications.models import JobApplication

        return list(JobApplication.objects.filter(applicant=obj).values_list('job_id', flat=True))

    def get_savedJobs(self, obj):
        from jobs.models import SavedJob

        return list(SavedJob.objects.filter(user=obj).values_list('job_id', flat=True))
User = get_user_model()
def send_email_async(subject, message, recipient_list):
    def _send():
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)
    thread = threading.Thread(target=_send)
    thread.start()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email address.")
        return value

    def save(self):
        email = self.validated_data['email']
        otp = ''.join(random.choices(string.digits, k=6))
        cache.set(f'reset_otp_{email}', otp, timeout=600)   # store OTP for 10 min

        # Send real email (no terminal)
        send_email_async(
            subject='Password Reset OTP',
            message=f'Your OTP for password reset is: {otp}',
            recipient_list=[email],
        )
        return otp   # still return for potential dev use, but not to frontend


# class ForgotPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         if not User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("No user with this email address.")
#         return value
#     def save(self):
#         email = self.validated_data['email']
#         user = User.objects.get(email=email)
        
#         otp = ''.join(random.choices('0123456789', k=6))
        
#         # For now (demo)
#         print(f"🔐 OTP for {email} is: {otp}")
        
#         # Send actual email
#         send_mail(
#             subject="Your Password Reset OTP",
#             message=f"Your OTP is: {otp}\nIt will expire in 10 minutes.",
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[email],
#             fail_silently=False,
#         )
#         return {"message": "OTP sent successfully", "otp": otp}  # Return in response
  
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "Passwords do not match."})
        return attrs

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)   # This is CRITICAL
            user.save()
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
