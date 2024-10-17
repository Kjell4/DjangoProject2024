from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Course, Video
from .models import Question, UserAnswer
from django.contrib.auth.decorators import login_required

@login_required
def take_test(request, slug):
    course = get_object_or_404(Course, slug=slug)

    serial_number = request.GET.get('lecture')
    if not serial_number:
        return redirect('course_page', slug=slug)

    video = get_object_or_404(Video, serial_number=serial_number, course=course)

    questions = video.questions.all()

    if not questions.exists():
        return render(request, 'exam/no_questions.html', {
            'video': video,
            'course': course,
            'error': "В тесте отсутствуют вопросы."
        })

    if request.method == 'POST':
        score = 0
        total_questions = questions.count()

        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option:
                selected_option = int(selected_option)  

                is_correct = selected_option == question.correct_option

                if is_correct:
                    score += 1

                UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct
                )

        result_message = f"{score} из {total_questions}"
        return render(request, 'exam/results.html', {
            'score': score,
            'total': total_questions,
             'course': course  
    })
    return render(request, 'exam/take_test.html', {
        'course': course,
        'video': video,
        'questions': questions
    })
