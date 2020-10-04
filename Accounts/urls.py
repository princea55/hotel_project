
from django.urls import path, include
from .views import login, signup, update,dashboard, logout, home, activate, password_reset_request
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),

    # login signup logout
    path('login/', login, name="login"),
    path('signup/', signup, name="signup"),
    path('logout/', logout, name="logout"),

    path('update/<int:pk>/', update, name="update"),
    path('', dashboard, name="dashboard"),

    #activate account
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    

    #password reset
    path("password_reset/",password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),      
    #social account login

    path('social-auth/', include('social_django.urls', namespace="social")),
    
]