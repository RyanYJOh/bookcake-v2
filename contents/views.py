from django.shortcuts import render, redirect
from .models import Comment, Content, Category, Book, BookThickness, Letter
from .forms import CommentForm, SearchForm
import json
from django.db.models import Q

# from .serializers import ContentSerializer, ContentsSerializer, CategorySerializer, BookSerializer, RcmndSerializer, BookThicknessSerializer, LetterSerializer
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# 한글 인코딩
import urllib.request
import urllib.parse

from django.utils import timezone
from datetime import datetime, date
from random import *
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

''' Base Settings START '''

''' Base Setting END '''

##### V2 #####

def book_search(form):
    if form.is_valid():
        keyword = form.cleaned_data['search_keyword']
        which = form.cleaned_data['which']

        if which == 'title':    
            cakes = Content.objects.filter(Q(source__title__icontains=keyword)).distinct().order_by('-pk')
            context = {
                'search_form' : form,
                'keyword' : keyword,
                'cakes' : cakes,
            }

        elif which == 'author' :
            cakes = Content.objects.filter(Q(source__author__icontains=keyword)).distinct().order_by('-pk')
            context = {
                'search_form' : form,
                'keyword' : keyword,
                'cakes' : cakes,
            }
            
        elif which == 'body' :
            cakes = Content.objects.filter(Q(body__icontains=keyword)).distinct().order_by('-pk')
            context = {
                'search_form' : form,
                'keyword' : keyword,
                'cakes' : cakes,
            }

        return context
    else:
        pass

def cake_list(request):
    ## Search
    # 답변 리스트 쿼리 -- 검색결과인지 여부 먼저 확인해야 함
    search_form = SearchForm(request.POST)
    print('METHOD.POST : ', request.POST)
    print('METHOD IS :  ', request.method)
    if request.method == 'POST':
        is_search_result=True
        
        search_context = book_search(search_form)
        print('SEARCH RESULT : ', search_context)
        cakes = search_context['cakes']
    
    else:
        is_search_result=False
        cakes_all = Content.objects.all().order_by('-pk')
        paginator_cakes = Paginator(cakes_all, 10)
        page_cakes = request.GET.get('page')
        cakes = paginator_cakes.get_page(page_cakes)
        
    ## Filter -- 카테고리 리스트
    cats = Category.objects.all()

    context = {
        'search_form' : search_form,
        'cakes' : cakes,
        'is_search_result' : is_search_result,
        'cats' : cats,
    }
    return render(request, 'contents/cake_list.html', context)

def cake_list_filtered(request, category):
    this_cat = Category.objects.get(pk=category)

    cakes_filtered = Content.objects.filter(category=this_cat.pk)
    paginator_cakes = Paginator(cakes_filtered, 10)
    page_cakes = request.GET.get('page')
    cakes = paginator_cakes.get_page(page_cakes)

    ## Filter -- 카테고리 리스트
    cats = Category.objects.all()
    
    is_filtered = True
    context = {
        'cakes' : cakes,
        'this_cat' : this_cat.category,
        'cats' : cats,
        'is_filtered' : is_filtered,
    }

    return render(request, 'contents/cake_list_filtered.html', context)

def each_cake(request, id): 
    if request.user.is_authenticated :
        user_is_ryan = True ## 멤버는 나밖에 없음
    else:
        user_is_ryan = False

    cake = Content.objects.get(pk=id)
    ryan_comment = cake.tmi

    ## comments
    comments = Comment.objects.filter(this_cake=cake)

    context = {
        'cake' : cake,
        'user_is_ryan' : user_is_ryan,
        'comments' : comments,
        'ryan_comment' : ryan_comment,
    }
    return render(request, 'contents/each_cake.html', context)

def book_list(request):
    books = Book.objects.all().order_by('-pk')
    paginator_books = Paginator(books, 15)
    page_books = request.GET.get('page')
    books_paginated = paginator_books.get_page(page_books)

    context = {
        'books_paginated' : books_paginated,
    }
    return render(request, 'contents/book_list.html', context)

def each_book(request, rcmnd_title):
    try:
        book = Book.objects.get(rcmnd_title=rcmnd_title)
    except ObjectDoesNotExist:
        return redirect('books')

    try:
        cakes = Content.objects.filter(source=book)
        cake_exists = True
    except ObjectDoesNotExist:
        cake_exists=False

    print(cake_exists)
    context = {
        'book' : book,
        'cake_exists' : cake_exists,
        'cakes' : cakes,
    }
    return render(request, 'contents/each_book.html', context)

def create_comment(request):
    print('댓글 작성 호출됨 ANS-US')
    data = json.loads(request.body)
    this_cake = data['this_cake']
    author = data['author']
    body = data['body']
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.this_cake = Content.objects.get(pk=this_cake)
            instance.body = body
            instance.author = author
        
            instance.save()
            print("댓글 작성 완료!")
                
            ## 아래 return 부분 잘 이해 안됨. return만 쓰면 에러 뜬다. 그렇다고 아래처럼 쓰면 아무런 반응 없음.
            return redirect('/me')
        else:
            print('@@@@@@ Validation failed due to : ', form.errors)
    else:
        pass

##############

##### REST API #####
''' 
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
''' 
####################