from django.shortcuts import render, redirect
from .models import Content, Category, Book, BookThickness, Letter
from .serializers import ContentSerializer, ContentsSerializer, CategorySerializer, BookSerializer, RcmndSerializer, BookThicknessSerializer, LetterSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

# 한글 인코딩
import urllib.request
import urllib.parse

from django.utils import timezone
from datetime import datetime, date
from random import *

''' Base Settings START '''

''' Base Setting END '''

''' REST API START '''
# API Overview
@api_view(['GET'])
def apiOverview(request):
    api_urls = { 
        'Home' : '/home/',
        'All contents' : '/cakes/',
        'Each content' : '/cake/<int:pk>/'
    }
    return Response(api_urls)

# /cakes
@api_view(['GET'])
def cake_list(request):
    # cat_num을 optional 매개변수로 쓰고 싶은데
    # if cat_num == '' or cat_num == '모두보기':
    #     cakes = Content.objects.all().order_by('-pk')
    # else:
    #     cakes = Content.objects.filter(category=cat_num).order_by('-pk')
    
    cakes = Content.objects.all().order_by('-pk')
    serialized = ContentsSerializer(cakes, many=True)

    return Response(serialized.data)

# /cake/pk
@api_view(['GET'])
def cake_each(request, pk):
    this_cake = Content.objects.get(pk=pk)
    serialized = ContentSerializer(
        this_cake, 
        context={
            'request':request,
            'cake' : this_cake
            },
    )
    return Response(serialized.data)

# GET Category
@api_view(['GET'])
def categories(request):
    categories = Category.objects.all()
    serialized = CategorySerializer(categories, many=True)
    
    return Response(serialized.data)

# GET Book
@api_view(['GET'])
def books(request):
    books = Book.objects.all()
    serialized = BookSerializer(books, many=True)
    
    return Response(serialized.data)

# GET Book
@api_view(['GET'])
def book_each(request, pk):
    this_book = Book.objects.get(pk=pk)
    serialized = BookSerializer(
        this_book, 
        context={
            'request':request,
            'book' : this_book
            },
    )
    
    return Response(serialized.data)

# GET Rcmnds -> books()와 동일, 하지만 is_rcmnded=True인 놈들만 가져옴
@api_view(['GET'])
def rcmnds(request):
    rcmnds = Book.objects.filter(is_rcmnded=True).order_by('?')
    serialized = BookSerializer(
        rcmnds, 
        context={'request':request, 'rcmnd':rcmnds}, 
        many=True)

    return Response(serialized.data)

# GET Rcmnd
@api_view(['GET'])
def rcmnd_each(request, rcmnd_title):
    this_rcmnd = Book.objects.get(rcmnd_title=rcmnd_title)
    serialized = RcmndSerializer(
        this_rcmnd,
        context={
            'request': request,
            'rcmnd' : this_rcmnd
        }
    )
    return Response(serialized.data)

# GET Thickness
@api_view(['GET'])
def thickness(request):
    thickness = BookThickness.objects.all()
    serialized = BookThicknessSerializer(thickness, many=True)
    
    return Response(serialized.data)

# GET Letter
@api_view(['GET'])
def letters(request):
    letter = Letter.objects.all().order_by('-id')
    serialized = LetterSerializer(letter, many=True)
    
    return Response(serialized.data)
''' REST API END '''