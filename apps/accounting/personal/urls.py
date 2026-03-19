from django.urls import path
from .views import AccoutingView, redirect_account

app_name = 'main'
urlpatterns = [
    path('', redirect_account, name='index'),
    path('<int:account_id>/', AccoutingView.as_view(), name='index_account'),
]
