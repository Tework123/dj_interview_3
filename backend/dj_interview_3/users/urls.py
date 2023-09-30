from django.urls import path

from users.views import UsersView, UsersEditView, UsersLogoutView, AuthUserView

urlpatterns = [

    path('', UsersView.as_view()),
    path('<int:pk>', UsersEditView.as_view()),
    path('auth/', AuthUserView.as_view()),
    path('logout/', UsersLogoutView.as_view()),

]
