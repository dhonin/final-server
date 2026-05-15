# # # # from rest_framework import viewsets, permissions
# # # # from rest_framework.decorators import action
# # # # from rest_framework.response import Response
# # # # from django_filters.rest_framework import DjangoFilterBackend
# # # # from rest_framework.filters import SearchFilter, OrderingFilter
# # # # from .models import Job
# # # # from .serializers import JobSerializer

# # # # class JobViewSet(viewsets.ModelViewSet):
# # # #     queryset = Job.objects.filter(is_active=True)
# # # #     serializer_class = JobSerializer
# # # #     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
# # # #     search_fields = ['title', 'company', 'description', 'location']
# # # #     ordering_fields = ['created_at', 'salary_min', 'salary_max']
# # # #     ordering = ['-created_at']

# # # #     def get_permissions(self):
# # # #         if self.action in ['create', 'update', 'partial_update', 'destroy']:
# # # #             return [permissions.IsAuthenticated()]
# # # #         return [permissions.AllowAny()]

# # # #     def perform_create(self, serializer):
# # # #         # Only HR can create a job
# # # #         if self.request.user.role != 'hr':
# # # #             raise PermissionError("Only HR can post jobs.")
# # # #         serializer.save(posted_by=self.request.user)

# # # #     @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
# # # #     def my_jobs(self, request):
# # # #         """Return jobs posted by the logged-in HR"""
# # # #         jobs = Job.objects.filter(posted_by=request.user)
# # # #         serializer = self.get_serializer(jobs, many=True)
# # # #         return Response(serializer.data)
# # # from rest_framework import viewsets, permissions
# # # from rest_framework.decorators import action
# # # from rest_framework.response import Response
# # # from django_filters.rest_framework import DjangoFilterBackend
# # # from rest_framework.filters import SearchFilter, OrderingFilter
# # # from .models import Job
# # # from .serializers import JobSerializer

# # # class JobViewSet(viewsets.ModelViewSet):
# # #     queryset = Job.objects.filter(is_active=True)
# # #     serializer_class = JobSerializer
# # #     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
# # #     search_fields = ['title', 'company', 'description', 'location']
# # #     ordering_fields = ['created_at', 'salary_min', 'salary_max']
# # #     ordering = ['-created_at']

# # #     def get_permissions(self):
# # #         if self.action in ['create', 'update', 'partial_update', 'destroy']:
# # #             return [permissions.IsAuthenticated()]
# # #         return [permissions.AllowAny()]

# # #     def perform_create(self, serializer):
# # #         if self.request.user.role != 'hr':
# # #             raise PermissionError("Only HR can post jobs.")
# # #         serializer.save(posted_by=self.request.user)

# # #     @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
# # #     def my_jobs(self, request):
# # #         jobs = Job.objects.filter(posted_by=request.user)
# # #         serializer = self.get_serializer(jobs, many=True)
# # #         return Response(serializer.data)
# # from rest_framework import viewsets, permissions
# # from rest_framework.decorators import action
# # from rest_framework.response import Response
# # from django_filters.rest_framework import DjangoFilterBackend
# # from rest_framework.filters import SearchFilter, OrderingFilter
# # from .models import Job
# # from .serializers import JobSerializer

# # class IsHROrReadOnly(permissions.BasePermission):
# #     """
# #     Custom permission: HR can do anything; others can only read (GET).
# #     """
# #     def has_permission(self, request, view):
# #         # SAFE_METHODS = GET, HEAD, OPTIONS
# #         if request.method in permissions.SAFE_METHODS:
# #             return True
# #         # Write methods: require authenticated user with role 'hr'
# #         return request.user.is_authenticated and request.user.role == 'hr'

# #     def has_object_permission(self, request, view, obj):
# #         # Read allowed for anyone
# #         if request.method in permissions.SAFE_METHODS:
# #             return True
# #         # Write/delete: only the HR who posted the job (owner) can modify
# #         return request.user == obj.posted_by

# # class JobViewSet(viewsets.ModelViewSet):
# #     queryset = Job.objects.filter(is_active=True)
# #     serializer_class = JobSerializer
# #     permission_classes = [IsHROrReadOnly]   # <-- enforce custom permission
# #     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
# #     search_fields = ['title', 'company', 'description', 'location']
# #     ordering_fields = ['created_at', 'salary_min', 'salary_max']
# #     ordering = ['-created_at']

# #     def perform_create(self, serializer):
# #         # The permission class already ensures request.user.role == 'hr'
# #         serializer.save(posted_by=self.request.user)

# #     @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
# #     def my_jobs(self, request):
# #         """Return jobs posted by the logged-in HR (only accessible to HR)"""
# #         if request.user.role != 'hr':
# #             return Response({'error': 'Only HR can access this endpoint.'}, status=403)
# #         jobs = Job.objects.filter(posted_by=request.user)
# #         serializer = self.get_serializer(jobs, many=True)
# #         return Response(serializer.data)
# from rest_framework import viewsets, permissions
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter, OrderingFilter
# from .models import Job
# from .serializers import JobSerializer

# class IsHROrReadOnly(permissions.BasePermission):
#     """
#     Only HR can create, update, delete jobs.
#     Seekers can only view (GET, HEAD, OPTIONS).
#     """
#     def has_permission(self, request, view):
#         # Read methods are safe for everyone
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         # Write methods require authenticated user with role 'hr'
#         return request.user.is_authenticated and request.user.role == 'hr'

#     def has_object_permission(self, request, view, obj):
#         # Read allowed for anyone
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         # Write/delete: only the HR who posted the job can modify it
#         return request.user == obj.posted_by

# class JobViewSet(viewsets.ModelViewSet):
#     queryset = Job.objects.filter(is_active=True)
#     serializer_class = JobSerializer
#     permission_classes = [IsHROrReadOnly]   # <-- apply custom permission
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     search_fields = ['title', 'company', 'description', 'location']
#     ordering_fields = ['created_at', 'salary_min', 'salary_max']
#     ordering = ['-created_at']

#     def perform_create(self, serializer):
#         # The permission class already restricts, but safe to keep
#         if self.request.user.role != 'hr':
#             raise PermissionError("Only HR can post jobs.")
#         serializer.save(posted_by=self.request.user)

#     @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
#     def my_jobs(self, request):
#         if request.user.role != 'hr':
#             return Response({'error': 'Only HR can access this endpoint.'}, status=403)
#         jobs = Job.objects.filter(posted_by=request.user)
#         serializer = self.get_serializer(jobs, many=True)
#         return Response(serializer.data)
#     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
#     def save(self, request, pk=None):
#         """Toggle save/unsave a job. POST /api/jobs/<id>/save/"""
#         job = self.get_object()
#         saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)
#         if not created:
#             saved.delete()
#             return Response({'saved': False, 'message': 'Job unsaved'}, status=200)
#         return Response({'saved': True, 'message': 'Job saved'}, status=201)

#     @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
#     def saved(self, request):
#         """List all jobs saved by the logged-in user. GET /api/jobs/saved/"""
#         saved_jobs = SavedJob.objects.filter(user=request.user)
#         serializer = SavedJobSerializer(saved_jobs, many=True)
#         return Response(serializer.data)
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Job, SavedJob
from .serializers import JobSerializer, SavedJobSerializer

class IsHROrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'hr'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.posted_by

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [IsHROrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'company', 'description', 'location']
    ordering_fields = ['created_at', 'salary_min', 'salary_max']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        if self.request.user.role != 'hr':
            raise PermissionError("Only HR can post jobs.")
        serializer.save(posted_by=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_jobs(self, request):
        if request.user.role != 'hr':
            return Response({'error': 'Only HR can access this endpoint.'}, status=403)
        jobs = Job.objects.filter(posted_by=request.user)
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)

    # -------- Saved Jobs Actions --------
    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def save(self, request, pk=None):
        """Save or unsave a job. POST/DELETE /api/jobs/<id>/save/"""
        job = self.get_object()
        if request.method == 'DELETE':
            SavedJob.objects.filter(user=request.user, job=job).delete()
            return Response({'saved': False, 'message': 'Job unsaved'}, status=status.HTTP_200_OK)

        saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)
        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response({'saved': True, 'message': 'Job saved'}, status=response_status)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def saved(self, request):
        """List all jobs saved by the logged-in user. GET /api/jobs/saved/"""
        saved_jobs = SavedJob.objects.filter(user=request.user)
        serializer = SavedJobSerializer(saved_jobs, many=True)
        return Response(serializer.data)
