from django.shortcuts import get_object_or_404, render, redirect
from courses.models import Course, Video
from user_payment.models import UserPayment
from django.urls import reverse
from exam.models import TestResult 
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def coursePage(request, slug):
    course = get_object_or_404(Course, slug=slug)
    serial_number = request.GET.get('lecture')

    # Получаем все видео для курса
    videos = course.video_set.all().order_by("serial_number")
    
    if serial_number is None:
        serial_number = 1

    video = get_object_or_404(Video, serial_number=serial_number, course=course)


    test_result = TestResult.objects.filter(user=request.user, video=video).first()

    user_payment = UserPayment.objects.filter(app_user=request.user, course=course, payment_bool=True).exists()
    
    if not user_payment and not video.is_preview:
        return redirect('product_page', slug=course.slug)

    context = {
        "course": course,
        "video": video,
        'videos': videos,
        'product_page_url': reverse('product_page', kwargs={'slug': course.slug}),
        'test_result': test_result, 
    }
    return render(request, template_name="courses/course_page.html", context=context)