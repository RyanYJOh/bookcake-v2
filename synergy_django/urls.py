from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from contents import views as content_view

urlpatterns = [
    # path('', TemplateView.as_view(template_name="index.html")),
    path('', include('main.urls')),
    # path('cakes/', content_view.cake_list, name="cake_list"),
    path('cakes/', content_view.cake_list, name='cake_list'),
    path('cakes/filter=<int:category>', content_view.cake_list_filtered, name='cake_list_filtered'),
    path('cake/<int:id>', content_view.each_cake, name="each_cake"),
    path('books/', content_view.book_list, name='book_list'),
    path('book/<str:rcmnd_title>', content_view.each_book, name="each_book"),
    path('inside-my-head', content_view.letter, name='letters'),

    ## 댓글
    path('ajax/create-comment', content_view.create_comment, name="create_comment"),

    # path('api/', include('contents.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
