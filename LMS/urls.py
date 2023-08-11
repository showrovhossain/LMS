from django.contrib import admin
from django.urls import path, include
from . import views, user_login
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),

    path('base/', views.BASE, name='base'),

    path('404', views.PAGE_NOT_FOUND, name='404'),

    path('', views.HOME, name='home'),

    path('courses/', views.SINGLE_COURSE, name='single_course'),

    path('course/<slug:slug>', views.COURSE_DETAILS, name='course_details'),

    path('courses/filter-data', views.filter_data, name="filter-data"),

    path('search', views.SEARCH_COURSE, name="search_course"),

    path('contact/', views.CONTACT_US, name='contact_us'),

    path('about/', views.ABOUT_US, name='about_us'),

    path('accounts/register/', user_login.REGISTER, name='register'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('dologin/', user_login.DO_LOGIN, name='dologin'),

    path('accounts/profile/', user_login.PROFILE, name='profile'),

    path('accounts/profile/update/', user_login.PROFILE_UPDATE, name='profile_update'),



    path('my_course', views.MY_COURSE, name='my_course'),



    path('order_completed/', views.order_completed, name='order_completed'),

    path('checkout/<slug:course_slug>/', views.checkout, name='checkout'),
    path('initiate_payment/<slug:course_slug>/', views.initiate_payment, name='initiate_payment'),
    path('payment_complete/', views.payment_complete, name='payment_complete'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)