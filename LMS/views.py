from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from app.models import Categories, Course, Level, Language, UserCourse, Video, Payment
from django.views import View
from unicodedata import category
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django.http import HttpResponse
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings

import requests
from .settings import *

from django.contrib.auth.decorators import login_required

from decimal import Decimal

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings







def BASE(request):
    return render(request, 'base.html')


def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')

    context = {
        'category': category,
        'course': course,
    }
    return render(request, 'Main/home.html', context)


def SINGLE_COURSE(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price = 0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    context = {
        'category':category,
        'level' : level,
        'course': course,
        'FreeCourse_count': FreeCourse_count,
        'PaidCourse_count' : PaidCourse_count,
    }

    return render(request, 'Main/single_course.html', context)


def filter_data(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    if price == ['PriceFree']:
       course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
       course = Course.objects.all()

    elif category:
        course = Course.objects.filter(category__id__in = category).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in = level).order_by('-id')

    context = {
        'course': course
    }
    t = render_to_string('ajax/course.html', context)
    return JsonResponse({'data': t})


def CONTACT_US(request):
    return render(request, 'Main/contact_us.html')


def ABOUT_US(request):
    return render(request, 'Main/about_us.html')

def SEARCH_COURSE(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)

    context = {
        'course':course,

    }
    return render(request, 'search/search.html',context)

def COURSE_DETAILS(request, slug):
    categories_instance = Categories()  # Create an instance of Categories
    categories = categories_instance.get_all_category()

    course = Course.objects.filter(slug=slug).first()

    if not course:
        return redirect('404')

    check_enroll = None
    if request.user.is_authenticated:
        try:
            user_id = request.user.id  # Get the user ID
            check_enroll = UserCourse.objects.get(user_id=user_id, course=course)
        except UserCourse.DoesNotExist:
            pass

    # Calculate the total time duration for the course
    time_duration = Video.objects.filter(course__slug=slug).aggregate(total_duration=Sum('time_duration'))

    context = {
        'course': course,
        'categories': categories,
        'time_duration': time_duration,  # Extract the total duration from the result dictionary
        'check_enroll': check_enroll,
    }
    return render(request, 'course/course_details.html', context)


def PAGE_NOT_FOUND(request):
    return render(request, 'error/404.html')







def MY_COURSE(request):
    course = UserCourse.objects.filter(user = request.user)

    course_count = course.count()
    context = {
        'course':course,
        'course_count': course_count,
    }

    return render(request, 'course/my_course.html',context)



def course_details(request, slug):
    course = Course.objects.get(slug=slug)
    lessons = Lesson.objects.filter(course=course)

    context = {
        'course': course,
        'lessons': lessons,
    }

    return render(request, 'course_details.html', context)


# Assuming you've imported necessary models and modules

def checkout(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    if course.price == 0:
        if request.user.is_authenticated:
            # Check if the user is already enrolled
            if not UserCourse.objects.filter(user=request.user, course=course).exists():
                user_course = UserCourse(user=request.user, course=course)
                user_course.save()
                messages.success(request, 'Course Successfully Enrolled!')
                return redirect('my_course')  # Redirect to my_course for free courses
            else:
                messages.warning(request, 'You are already enrolled in this course.')
        else:
            messages.warning(request, 'Please log in to enroll in this course.')
            return redirect('login')  # Redirect to the login page


    context = {
        'course': course
    }
    return render(request, 'checkout/checkout.html', context)


def initiate_payment(request, course_slug):
    try:
        course = get_object_or_404(Course, slug=course_slug)
    except Course.DoesNotExist:
        return render(request, 'checkout/error.html', {'message': 'Course not found'})

    # Replace with your SSLCommerz credentials
    store_id = "test64d5325d56ad7"
    store_passwd = "test64d5325d56ad7@ssl"
    total_amount = course.price  # Replace with the actual course price

    post_data = {
        'store_id': store_id,
        'store_passwd': store_passwd,
        'total_amount': total_amount,
        'currency': 'BDT',
        'tran_id': str(course_id),  # Use course_id as the transaction ID
        # Add more required parameters based on your needs
    }

    response = requests.post(settings.SSLCOMMERZ_GATEWAY, data=post_data)

    if response.status_code == 200:
        # Process the SSLCommerz response, save payment information, etc.
        payment = Payment.objects.create(
            order_id=course_id,
            payment_id=response.json().get('val_id'),
            user=request.user,
            amount=total_amount,
        )
        # Redirect to SSLCommerz payment gateway
        return redirect(response.json().get('GatewayPageURL'))
    else:
        # Handle error
        messages.error(request, 'Failed to initiate payment')
        return redirect('checkout', course_slug=course.slug)

def payment_complete(request):
    # Handle SSLCommerz success response
    # Update payment status, grant access to the course, etc.
    return render(request, 'payment/success.html', {'message': 'Payment completed successfully'})

def payment_cancelled(request):
    # Handle SSLCommerz payment cancellation
    # Update payment status, handle cancellation, etc.
    return render(request, 'payment/cancelled.html', {'message': 'Payment was cancelled'})

def order_completed(request):
    return render(request, 'checkout/order_completed.html')





