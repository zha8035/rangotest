from django.urls import path
from rango import views
from rango.views import AboutView
app_name='rango'
urlpatterns=[
    path('',views.index,name='index'),
    #path('about/',views.about,name='about'),
    path('about/',views.AboutView.as_view(),name='about'),
    path('category/<slug:category_name_slug>/',views.show_category,name='show_category'),
    #path('add_category/',views.add_category,name='add_category'),
    path('add_category/',views.AddCategoryView.as_view(),name='add_category'),
    path('category/<slug:category_name_slug>/add_page/',views.add_page,name='add_page'),
    # path('register/',views.register,name='register'), # New mapping
    # path('login/',views.user_login,name='login'),
    path('restricted/',views.restricted,name='restricted'),
    #path('search/',views.search,name='search'),
    path('goto',views.goto_url,name='goto'),
    # path('logout',views.user_logout,name='logout'),
    path('register_profile/',views.register_profile,name='register_profile'),
    path('profile/<username>/',views.ProfileView.as_view(),name='profile'),
    path('profiles/',views.ListProfilesView.as_view(),name='list_profiles'),
    path('like_category/',views.LikeCategoryView.as_view(),name='like_category'),
    path('suggest/',views.CategorySuggestionView.as_view(),name='suggest'),
]