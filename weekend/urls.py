# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 21:56:37 2018

@author: Prasad
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from weekend import views

urlpatterns = [
    url(r'^admin/$', admin.site.urls),
    url(r'homee/',views.show_html),
    
    url(r'high/', views.high),
    url(r'low/', views.low)    
]
