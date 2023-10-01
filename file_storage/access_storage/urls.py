from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.urls import re_path

router = DefaultRouter()
router.register(r'upload-file',UploadFile)
router.register(r'list-uploaded-file',ListUploadedFile)
router.register(r'download-file', DownloadFile)

urlpatterns = [
	path('', include(router.urls)),
    path('download-file/<int:pk>/download/', DownloadFile.as_view({'get': 'download_file'}), name='download-file'),
    path('signup/', Signup.as_view()),
    re_path('verification/(?P<random_string>\w{10})/$', verification.as_view())
]