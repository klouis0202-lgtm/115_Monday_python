from django.urls import path

from .views import GoHomeView, HomeView, TextResponseView, JsonResponseView, GreetingView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("text/", TextResponseView.as_view(), name="text"),
    path("json/", JsonResponseView.as_view(), name="json"),
    path("auhfuhqf/", GoHomeView.as_view(), name="go_home"),
    path("greeting/", GreetingView.as_view(), name="greeting"),



]
