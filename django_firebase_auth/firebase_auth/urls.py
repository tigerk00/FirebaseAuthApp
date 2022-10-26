from django.urls import path
from .views import AuthRegister, CreateTokenView, UserView, CurrentUserInfoView, UsersListView, users_list_firebase


app_name = 'firebase_auth'

urlpatterns = [
    path('register/', AuthRegister.as_view(), name="auth-register"),
    path('get_token/', CreateTokenView.as_view(), name="auth-token"),
    path('users_list/', UsersListView.as_view(), name="users-list"),
    path('current_user_info/', CurrentUserInfoView.as_view(), name="current-user-info"),
    path('user/<str:pk>', UserView.as_view(), name="user"),
    path('users_list/', UsersListView.as_view(), name="users-list"),
    path('users_list_firebase/', users_list_firebase, name="users-list-firebase"),
]