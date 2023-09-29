from django.urls import path

from users.views import UsersView, UsersEditView

urlpatterns = [

    # показывает информацию об аккаунте
    path('', UsersView.as_view()),
    path('<int:pk>', UsersEditView.as_view()),

]
