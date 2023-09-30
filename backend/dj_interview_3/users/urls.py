from django.urls import path, re_path

from users.views import (UsersView, UsersEditView, UsersLogoutView,
                         AuthUserView, UsersFilterView, UsersOrderView)

urlpatterns = [

    path('', UsersView.as_view()),
    re_path(r'^filter/(?P<email>[\w.@+-]+)/', UsersFilterView.as_view()),
    re_path(r'^order_by/(?P<order_by>[\w.@+-]+)/', UsersOrderView.as_view()),
    path('<int:pk>', UsersEditView.as_view()),
    path('auth/', AuthUserView.as_view()),
    path('logout/', UsersLogoutView.as_view()),

]
