from django.contrib import admin
from django.urls import path
from home import views

admin.site.site_header="Let's Shop"
admin.site.site_title="Lets's Shop"
admin.site.index_title="Let's Shop"

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('collection', views.collection, name='collection'),
    path('collectionview/<str:slug>', views.collectionview, name='collectionview'),
    path('collectiondetail/<str:slugc>/<str:slugp>', views.collectiondetail, name='collectiondetail'),
    path('fnlogin', views.fnlogin, name='fnlogin'),
    path('fnlogout', views.fnlogout, name='fnlogout'),
    path('addtocart', views.addtocart, name='addtocart'),
    path('cartpage', views.cartpage, name='cartpage'),
    path('removecart/<str:id>', views.removecart, name='removecart'),
    path('favourite', views.favourite, name='favourite'),
    path('favouritepage', views.favouritepage, name='favouritepage'),
    path('removefavourite/<str:id>', views.removefavourite, name='removefavourite'),
    path('search', views.search, name='search'),
    path('buy', views.buy, name='buy'),
]
