from django.urls import path
from .views import AdminAddUserView, ActivateUserView, SetPasswordView

urlpatterns = [
    path("admin/add-user/", AdminAddUserView.as_view()),
    path("activate/<int:uid>/<str:token>/", ActivateUserView.as_view()),
    path("set-password/", SetPasswordView.as_view(), name="set-password"),
]
