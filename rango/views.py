from django.shortcuts import render,redirect
from django.urls import reverse
# Create your views here.
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm,PageForm
from rango.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from rango.models import UserProfile

def index(request):
    #return HttpResponse('Rango says hey there partner!    <a href="/rango/about/">About</a>')
    #query the database for a list of all categories currently stored
    #order the categories by the number of likes in descending order
    #retrive the top 5 only--or all if less than 5
    #place the list in our context_dict dictionary (with our bold message)
    #that will be passed to the template engine
    category_list=Category.objects.order_by('-likes')[:5]
    page_list=Page.objects.order_by('-views')[:5]
    context_dict={}
    context_dict['boldmessage']='Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories']=category_list
    context_dict['pages']=page_list
    #context_dict['visits']=int(request.COOKIES.get('visits',1))
    visitor_cookie_handler(request)
    #context_dict['visits']=request.session['visits']
    #context_dict={'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!'}
    #render the response and send it back
    #request.session.set_test_cookie()
    #obtian our response object early so we can add cookie info
    response=render(request,'rango/index.html',context_dict)
    #call the helper function to handle the cookies
    
    #return response banck to the user,updating any cookies that need changed
    return response
    #return render(request,'rango/index.html',context=context_dict)
def about(request):
    context_dict={'boldmessage':'Huixiong Zhang'}
    # if request.session.test_cookie_worked():
    #     print("Test Cookie Worked!")
    # request.session.delete_test_cookie()
    visitor_cookie_handler(request)
    context_dict['visits']=request.session['visits']
    return render(request, 'rango/about.html',context=context_dict)
def show_category(request,category_name_slug):
    #creare a context dictionary which we can pass
    # to the template rendeing engine
    context_dict={}
    try:
        #can we find a category slug with the given name?
        #if we cannot, the .get() method raises a dosenotexist exception
        #so the .get() method returns one model instance or raises an exception
        category=Category.objects.get(slug=category_name_slug)
        #retrive all of the associated pages
        #note that filter() will return a list of page objects or an empty list
        pages=Page.objects.filter(category=category).order_by('-views')
        #add our results list to the template context under name pages
        context_dict['pages']=pages
        #we also add the category object from the database to the dictionary
        #we will use this in the template to verify that the category exists
        context_dict['category']=category
    except Category.DoesNotExist:
        #we get here if we did not find thet specified category
        # don't do anything
        # the template will display the no category message for Us
        context_dict['category']=None
        context_dict['pages']=None
    # start new search functionality
    if request.method == 'POST':
        query=request.POST['query'].strip()
        if query:
            #run our bing function to get the results list!
            context_dict['result_list']=run_query(query)
            context_dict['query']=query
    #render the response and return it ti the client
    return render(request,'rango/category.html',context_dict)
def add_category(request):
    form=CategoryForm()
    #A HTTP POST?
    if request.method=='POST':
        form=CategoryForm(request.POST)
        #have we been provided a valid form?
        if form.is_valid():
            #save the new category to the database
            cat=form.save(commit=True)
            print(cat,cat.slug)
            #now the category is saved
            #we could give a confirmation message
            #but since the most recent category added is on the index page
            #we can direct the user back to the index page
            return index(request)
        else:
            #the supplied form contained errors-
            #just print them to the terminal
            print(form.errors)
    #Will handle the bad form,new form, or no form supplied cases
    #render the form with error messages(if any)
    return render(request,'rango/add_category.html',{'form':form})
def add_page(request,category_name_slug):
    try:
        category=Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category=None
    form=PageForm()
    if request.method=='POST':
        form=PageForm(request.POST)
        if form.is_valid():
            if category:
                page=form.save(commit=False)
                page.category=category
                page.views=0
                page.save()
                return redirect(reverse('rango:show_category',kwargs={'category_name_slug':category_name_slug}))
            else:
                print(form.errors)
    context_dict={'form':form,'category':category}
    return render(request,'rango/add_page.html',context_dict)

# def register(request):
#     #a boolean value for telling the template
#     # whether the registration wa successful
#     # set to false initially code changes to true when registration succeeds
#     registered=False
#     #if it is a http post,we are interested in processing form data
#     if request.method == 'POST':
#         #attempt to grab info from the raw form info
#         #print('AAAAAAAAAAA')
#         #note that we make use of both UserForm and UserProfileForm
#         user_form=UserForm(data=request.POST)
#         profile_form=UserProfileForm(data=request.POST)
#         #if the two forms are valid
#         if user_form.is_valid() and profile_form.is_valid():
#             #save the user's form data to the database
#             user=user_form.save()
#             #now hash the password with the setpassword method
#             # once hashed,we can update the userobject
#             user.set_password(user.password)
#             user.save()
#             #now sort out the UserProfile instance
#             # since we need to set the user attribute ourselves
#             # we set commit=false this delays saving the model
#             # until we are ready to avoid integrity problems
#             profile=profile_form.save(commit=False)
#             profile.user=user
#             #did the user provide a profile picture?
#             # if so,we need to et it from the unput form and put it in te UserProfile model
#             if 'picture' in request.FILES:
#                 profile.picture=request.FILES['picture']
#             #now we save the UserProfile model instance
#             profile.save()
#             #update our variable to indicate that the template registration was successful
#             registered=True
#         else:
#             #invalid form or forms-mistakes or somethingelse
#             #print problems to the terminal
#             print(user_form.errors,profile_form.errors)
#     else:
#         #not a post so we render our form using two ModelForm instances
#         #these forms will be blank ready for user input
#         user_form=UserForm()
#         profile_form=UserProfileForm()
#     #render the template depending on the context
#     return render(request,'rango/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

# def user_login(request):
#     #if the request is a POST try to pull out the relevent information
#     if request.method == 'POST':
#         #gather the username and password provided by the user
#         #this info is obtained from the login form
#         #we use request.POST['<variable>'] brvsudr the request.POST.get['']returns None if 
#         #the value does not exist,while request.POST[] will raise a keyerror exception
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         #use django's machinery to attempt to see if the username/password combination is valid
#         # a user object is returned if it is
#         user=authenticate(username=username,password=password)
#         #if we have a user object, the detail are correct
#         # if None(python's way of representing the abscence of a value) no user
#         #with matching credentials was found
#         if user:
#             #is the account active? it could have been disabled
#             if user.is_active:
#                 #if the account is valid and active we can log the user in
#                 #we will send the user back to the homepage
#                 login(request,user)
#                 print("AAAAAAAAAAA")
#                 return redirect(reverse('rango:index'))
#             else:
#                 #an inactive account was used-no logging in
#                 return HttpResponse("Your rango account is diabled.")
#         else:
#             #bad login detais were provided. so we can't log the user in
#             print("invalid login details:{0},{1}".format(username,password))
#             return HttpResponse('Invalid login details supplied')
#     #the request is not a post, so display the login form
#     # this scenario would most likelu be a get
#     else:
#         #no context variable to pass to the template system,hence the blank dictionary object...
#         return render(request,'rango/login.html')
def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse('You are logged in')
    else:
        return HttpResponse('You are not logged in')

@login_required
def restricted(request):
    #return HttpResponse("Since you are logged in, you can see this text")
    return render(request,'rango/restricted.html')
# @login_required
# def user_logout(request):
#     #since we know the user is logged in,we can now just log them out
#     logout(request)
#     return redirect(reverse('rango:index'))

def visitor_cookie_handler(request):
    #get the number of visites to the site
    #we use the cookies.get function to obtain the visits cookie
    #if the cookie exists,the value returned is casted to an integer
    # if the cookie does not exist, then the default value of 1 is used
    visits=int(request.COOKIES.get('visits','1'))
    last_visit_cookie=request.COOKIES.get('last_visit',str(datetime.now()))
    last_visit_time=datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    #if it has been more than a day since the last visit...
    if (datetime.now()-last_visit_time).days>0:
        visits=visits+1
        #update the last visit cookie now that we have uodated the count
        #response.set_cookie('last_visit',str(datetime.now()))
        request.session['last_visit']=str(datetime.now())
    else:
        #set the last visit cookie
        #response.set_cookie('last_visit',last_visit_cookie)
        request.session['last_visit']=last_visit_cookie
    #update set the visits cookie
    #response.set_cookie('visits',visits)
    request.session['visits']=visits

# a helper method
def get_server_side_cookie(request,cookie,default_val=None):
    val=request.session.get(cookie)
    if not val:
        val=default_val
    return val
# def search(request):
#     result_list=[]
#     query=None
#     if request.method=='POST':
#         query=request.POST['query'].strip()
#         if query:
#             #run our bing function to get the results list!
#             result_list=run_query(query)
#     return render(request,'rango/search.html',{'result_list':result_list,'query':query})
def goto_url(request):
    #get pageid /rango/goto/?page_id=1
    #page_id=None
    if request.method=='GET':
        page_id=request.GET.get('page_id')
        try:
            selected_page=Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('rango:index'))
        selected_page.views=selected_page.views+1
        selected_page.save()
        return redirect(selected_page.url)
    return redirect(reverse('rango:index'))
    #get() the page with an id of page_id(from the get request)
    #for that particular instance,increment the views by one and then
    #save the changes 
    #after that,redirect
    #if page is NA, redirect to homepage
    #redirect helper function and the reverse()
    #use try except

    # url

    #category.htm. link the goto_url view

    #update category.html to also report the number of views that page receive
    # singular and plural
    #update show_category() 
@login_required
def register_profile(request):
    form=UserProfileForm()
    if request.method=='POST':
        form=UserProfileForm(request.POST,request.FILES)
        if form.is_valid():
            user_profile=form.save(commit=False)
            user_profile.user=request.user
            user_profile.save()
            return redirect('rango:index')
        else:
            print(form.errors)
    context_dict={'form':form}
    return(request,'rango/profile_registration.html',context_dict)

class AboutView(View):
    def get(self,request):
        context_dict={}
        context_dict['visits']=request.session['visits']
        return render(request,'rango/about.html',context_dict)
        
class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self,request):
        form=CategoryForm()
        return render(request,'rango/add_category.html',{'form':form})
    @method_decorator(login_required)
    def post(self,request):
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
        return render(request,'rango/add_category.html',{'form':form})
class ProfileView(View):
    def get_user_details(self,username):
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        userprofile=UserProfile.objects.get_or_create(user=user)[0]
        form=UserProfileForm({'website':userprofile.website,'picture':userprofile.picture})
        return (user,userprofile,form)
    @method_decorator(login_required)
    def get(self,request,username):
        try:
            (user,userprofile,form)=self.get_user_details(username)
        except TypeError:
            return redirect('rango:index')
        context_dict={'userprofile':userprofile,'selecteduser':user,'form':form}
        return render(request,'rango/profile.html',context_dict)
    @method_decorator(login_required)
    def post(self, request,username):
        try:
            (user,userprofile,form)=self.get_user_details(username)
        except TypeError:
            return redirect('rango:index')
        form=UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile',user.username)
        else:
            print(form.errors)
        context_dict={'userprofile':userprofile,'selecteduser':user,'form':form}
        return render(request,'rango/profile.html',context_dict)
class ListProfilesView(View):
    @method_decorator(login_required)
    def get(self,request):
        profiles=UserProfile.objects.all()
        return render(request,'rango/list_profiles.html',{'userprofile_list':profiles})
#class LikeCategoryView(View):
# class LikeCategoryView(View):
#     @method_decorator(login_required)
#     def get(self,request):
#         category_id=request.GET['category_id']
#         try:
#             category=Category.objects.get(id=int(category_id))
#         except Category.DoesNotExist:
#             return HttpResponse(-1)
#         except ValueError:
#             return HttpResponse(-1)
#         category.likes=category.likes+1
#         category.save()
#         return HttpResponse(category.likes)

class LikeCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        category_id = request.GET['category_id']
        
        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        category.likes = category.likes + 1
        category.save()
        
        return HttpResponse(category.likes)

def get_category_list(max_results=0,starts_with=''):
    category_list=[]
    if starts_with:
        category_list=Category.objects.filter(name__istartswith=starts_with)
    if max_results>0:
        category_list=category_list[:max_results]
    return category_list



# def get_category_list(max_results=0, starts_with=''):
#     category_list = []
    
#     if starts_with:
#         category_list = Category.objects.filter(name__istartswith=starts_with)
    
#     if max_results > 0:
#         if len(category_list) > max_results:
#             category_list = category_list[:max_results]
    
#     return category_list

class CategorySuggestionView(View):
    def get(self,request):
        suggestion=request.GET['suggestion']
        category_list=get_category_list(max_results=8,starts_with=suggestion)
        if len(category_list)==0:
            category_list=Category.objects.order_by('-likes')
        return render(request,'rango/categories.html',{'categories':category_list})

# class CategorySuggestionView(View):
#     def get(self, request):
#         suggestion = request.GET['suggestion']
#         category_list = get_category_list(max_results=8, starts_with=suggestion)
        
#         if len(category_list) == 0:
#             category_list = Category.objects.order_by('-likes')
        
#         return render(request, 'rango/categories.html', {'categories': category_list})








