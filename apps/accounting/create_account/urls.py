from django.urls import path
from django.views.generic import TemplateView

from .views import CreatePersonalAccountView

app_name = "new_account"

urlpatterns = [
    path('', TemplateView.as_view(template_name="create_add_account.html"), name="create"),
    path('create/', CreatePersonalAccountView.as_view(), name='create_account')
]
