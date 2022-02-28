from django.shortcuts import render

# from bookcake_django.bookcake.contents.models import Book, Content

# Create your views here.

##### 공통 #####
'''
def navbar(request):
    # navbar_this_user = User.objects.get(user=request.user)
    if request.user.is_authenticated:
        navbar_authenticated = True
        navbar_this_user = request.user
        # try:
        #     navbar_this_userinfo = UserInfo.objects.get(this_user=navbar_this_user)
        #     navbar_authenticated = 'True'

        #     navbar_context = {
        #         'navbar_authenticated' : navbar_authenticated,
        #         'navbar_this_user' : navbar_this_user.username,
        #         'navbar_this_userinfo' : navbar_this_userinfo,
        #     }
        # except ObjectDoesNotExist:
            # navbar_authenticated = 'False'
            # navbar_context = {
            #     'navbar_authenticated' : navbar_authenticated,
            #     'navbar_this_user' : navbar_this_user.username,
            # }
    else:
        navbar_authenticated = False

        navbar_context = {
            'navbar_authenticated' : navbar_authenticated,
        }
    
    return navbar_context
'''   

def home(request):
    # navbar_context = navbar(request)

    pre_context = {
        
    }

    # context = {**navbar_context, **pre_context}
    return render(request, 'main/home.html', pre_context)