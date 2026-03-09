from django.urls import path
from storage.views import StorageView

urlpatterns = [
    path("api/store/", StorageView.as_view()),
    path("api/store/<str:filename>", StorageView.as_view()),
]
