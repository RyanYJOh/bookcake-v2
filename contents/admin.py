from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Content, Book, Category, BookThickness, Letter

# Apply summernote to all TextField in model.
class ContentAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

class BookAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(Content, ContentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Category)
admin.site.register(BookThickness)
admin.site.register(Letter)
