from django.shortcuts import render, redirect
from courses.models import Course, Video
from user_payment.models import UserPayment
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def coursePage(request, slug):
    course = Course.objects.get(slug=slug)
    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by("serial_number")
    product_page_url = reverse('product_page', kwargs={'slug': course.slug})

    if serial_number is None:
        serial_number = 1

    try:
        video = Video.objects.get(serial_number=serial_number, course=course)
    except Video.DoesNotExist:
        return redirect('course_page', slug=course.slug)

    user_payment = UserPayment.objects.filter(app_user=request.user, course=course, payment_bool=True).exists()
    
    if not user_payment and not video.is_preview:
        return redirect('product_page', slug=course.slug)
    
    context = {
        "course": course,
        "video": video,
        'videos': videos,
        'product_page_url': product_page_url,
    }
    return render(request, template_name="courses/course_page.html", context=context)
