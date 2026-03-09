from django.urls import path
from cipher.views import CipherView

urlpatterns = [
    path("api/store/", CipherView.as_view()),
    path("api/store/<str:filename>", CipherView.as_view()),
]
