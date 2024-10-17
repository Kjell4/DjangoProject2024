from django.shortcuts import render, redirect
from courses.models import Course, Video
from user_payment.models import UserPayment
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def coursePage(request, slug):
    course = Course.objects.get(slug=slug)
    serial_number = request.GET.get('lecture')

    # Получаем все видео для курса
    videos = course.video_set.all().order_by("serial_number")
    
    if serial_number is None:
        serial_number = 1

    try:
        # Пытаемся получить видео по серийному номеру
        video = Video.objects.get(serial_number=serial_number, course=course)
    except Video.DoesNotExist:
        return redirect('course_page', slug=course.slug)

    user_payment = UserPayment.objects.filter(app_user=request.user, course=course, payment_bool=True).exists()
    
    if not user_payment and not video.is_preview:
        return redirect('product_page', slug=course.slug)
    
    # Проверяем, является ли текущая лекция последней
    if serial_number and int(serial_number) == videos.count():
        # Перенаправляем на тест после последнего видео
        return redirect('take_test', video_id=video.id)

    context = {
        "course": course,
        "video": video,
        'videos': videos,
        'product_page_url': reverse('product_page', kwargs={'slug': course.slug}),
    }
    return render(request, template_name="courses/course_page.html", context=context)
