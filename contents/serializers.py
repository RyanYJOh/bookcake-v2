from rest_framework import serializers
from .models import Content, Category, Book, BookThickness, Letter

class BookThicknessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookThickness
        fields = ['id', 'thickness']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'cover', 'title', 'author', 'publisher', 'url',
        'rcmnd_title', 'rcmnd_whom', 'rcmnd_introduction',]

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category']

class ContentsSerializer(serializers.ModelSerializer):
    # 'category'가 Category 모델의 id가 아닌 string값으로 serialize 되도록
    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Content
        fields = [
            'id', 'source', 'category', 'key_line', 'body', 'tmi', 'footnote', 'created_at', 'image'
            ]

class ContentSerializer(serializers.ModelSerializer):
    # Foreign Key에서 특정 필드 보여주기
    source_title = serializers.SerializerMethodField()
    source_url = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = [
            'id', 'source', 'category', 'key_line', 'body', 'tmi', 'footnote', 'created_at', 'image',
            'source_title', 'source_url'
            ]

    def get_source_title(self, obj):
        this_title = self.context['cake'].source.title
        this_author = self.context['cake'].source.author
        return this_author + ", <" + this_title + ">"
    
    def get_source_url(self, obj):
        return self.context['cake'].source.url

class RcmndSerializer(serializers.ModelSerializer):
    # Foreign Key에서 특정 필드 보여주기
    thickness = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'cover', 'title', 'author', 'publisher', 'url',
        'is_rcmnded', 'rcmnd_title', 'rcmnd_thickness', 'rcmnd_whom', 'rcmnd_introduction', 'rcmnd_body',
        'thickness', ]
    
    def get_thickness(self, obj):
        this_thickness = self.context['rcmnd'].rcmnd_thickness.thickness
        return this_thickness

class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ['id', 'title', 'created_at', 'url', 'is_hot']