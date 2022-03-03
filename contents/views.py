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

def letter(request):
    all_letters = Letter.objects.all().order_by('-published_at')
    paginator_letters = Paginator(all_letters, 12)
    page_letters = request.GET.get('page')
    letters = paginator_letters.get_page(page_letters)

    context = {
        'letters' : letters,
    }

    return render(request, 'contents/my_head.html', context)
##############
