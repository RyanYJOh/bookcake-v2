from django.db import models
from django.utils import timezone

class Category(models.Model):
    # objects = models.Manager
    category = models.CharField(max_length = 20)

    def __str__(self):
        return self.category

class BookThickness(models.Model):
    objects = models.Manager()

    thickness = models.CharField(max_length=20)

    def __str__(self):
        return self.thickness

class Book(models.Model):
    objects = models.Manager()
    cover = models.ImageField(upload_to="None", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    title = models.CharField(max_length = 30)
    author = models.CharField(max_length = 20)
    publisher = models.CharField(max_length = 10)
    url = models.URLField()

    is_rcmnded = models.BooleanField(default=False)
    review_url = models.URLField()
    rcmnd_title = models.CharField(max_length = 30, null=True, blank=True)
    rcmnd_thickness = models.ForeignKey("BookThickness", null=True, blank=True, on_delete=models.CASCADE)
    rcmnd_whom = models.TextField(null=True, blank=True)
    rcmnd_introduction = models.TextField(null=True, blank=True)
    rcmnd_body = models.TextField(null=True, blank=True)
    review_url = models.URLField(null=True)

    def __str__(self):
        return self.title

class Content(models.Model):
    # objects = models.Manager()

    # 화면에 display
    source = models.ForeignKey("Book", related_name='book', on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='None', height_field=None, width_field=None, max_length=None, null=True, blank=True)
    key_line = models.CharField(max_length = 100, null=True)
    body = models.TextField(blank=True, null=True)
    tmi = models.TextField(blank=True, null=True)
    footnote = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)

    # 외적인 기능
    keywords = models.CharField(max_length = 100, blank=True, null=True)     ### 검색시 사용 (comma-separated)
    title = models.CharField(max_length=30, blank=True, null=True)  ### 어드민 페이지에 보여질 오브젝트 이름
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    objects = models.Manager()
    this_cake = models.ForeignKey("Content", related_name='content', on_delete=models.CASCADE)
    author = models.CharField(max_length=25, blank=True)
    body = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)

class Letter(models.Model):
    objects = models.Manager()
    cover = models.ImageField(upload_to="letter", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    title = models.CharField(max_length = 30)
    published_at = models.DateField(auto_now_add=False)
    url = models.URLField()
    is_hot = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' (' + str(self.published_at) + ')'