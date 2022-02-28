from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # path('', views.apiOverview, name="api-overview"),  
    # path('cakes/', views.cake_list, name="cakes"),
    # path('cake/<int:pk>', views.cake_each, name="each cake"),
    # path('categories/', views.categories, name="categories"),
    # path('books/', views.books, name="books"),
    # path('book/<int:pk>', views.book_each, name="each book"),
    # path('you-may-like-these/', views.rcmnds, name="recommendations"),
    # path('you-may-like/<str:rcmnd_title>', views.rcmnd_each, name="each rcmnd"),
    # path('thickness/', views.thickness, name="thickness"),
    # path('inside-my-head/', views.letters, name="letters"),
]
