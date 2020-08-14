from django.contrib import admin
from django.urls import path, include
from . import views
from .dash_collection import dash_1
from .dash_collection import dash_1_1
from .dash_collection import dash_2
from .dash_opioid_epidemic import app
from .OE_2 import app
from .dash_collection import dash_3
from .dash_collection import dash_4
from .dash_collection import dash_5
from .dash_collection import dash_cb_1
from .dash_collection import dash_cb_4
from django.views.generic.base import TemplateView
from two_factor.urls import urlpatterns as tf_urls


app_name = 'a_thing'
urlpatterns = [
    path('edit/', views.edit, name='edit'),
    path('register/', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/bio/', views.BioView.as_view(), name='bio'),

    path('dash_1/', views.dash_1, name="dash_1"),
    path('dash_2/', views.dash_2, name="dash_2"),
    path('dash_3/', views.dash_3, name="dash_3"),
    path('dash_4/', views.dash_4, name="dash_4"),
    path('dash_5/', views.dash_5, name="dash_5"),

    path('dash_cb_1/', views.dash_cb_1, name="dash_cb_1"),

    path('dash_OE', views.dash_OE, name="dash_OE"),
    path('dash_OE_2', views.dash_OE_2, name="dash_OE_2"),

    path('dash_cb_4', views.dash_cb_4, name="dash_cb_4"),

    # Bookmarks
    path('', views.home, name="home"),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('two_factor/', include(tf_urls)),

    path('tw/', views.tw, name='tw'),

    path('verification/', views.phone_verification, name="phone_verification"),

    path('verification/token/', views.token_validation, name="token_validation"),

    path('verified/', views.verified, name='verified')
]







