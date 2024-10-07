from django.shortcuts import render
from courses.models import Course , Video
from django.shortcuts import HttpResponse


def coursePage(request, slug):
    course = Course.objects.get(slug = slug)
    serial_number = request.GET.get('lecture')

    if serial_number is None:
        serial_number = 1
    video = Video.objects.get(serial_number = serial_number, course = course)
    context = {
        "course" : course,
        "video" : video
    }
    return render(request, template_name="courses/course_page.html", context=context)