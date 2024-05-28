from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.MainPageView.as_view()),
    path('cap_detail/<slug:slug>/', views.StorageDetailListView.as_view()),
    path('cap_list/', views.StorageListView.as_view()),
    path('buy_cap/', views.BasketCreateView.as_view()),
]

