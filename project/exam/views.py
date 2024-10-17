from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Course, Video
from .models import Question, Choice, UserAnswer
from django.contrib.auth.decorators import login_required


@login_required
def take_test(request, slug):
    course = get_object_or_404(Course, slug=slug)

    serial_number = request.GET.get('lecture')
    if not serial_number:
        return redirect('course_page', slug=slug)

    video = get_object_or_404(Video, serial_number=serial_number, course=course)

    # Получаем вопросы, связанные с видео
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
            selected_choice_id = request.POST.get(str(question.id))
            if selected_choice_id:
                selected_choice = get_object_or_404(Choice, id=selected_choice_id)
                is_correct = selected_choice.is_correct
                if is_correct:
                    score += 1

                # Сохранение ответа пользователя
                UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    selected_choice=selected_choice,
                    is_correct=is_correct
                )

        final_score = (score / total_questions) * 100
        return render(request, 'exam/results.html', {'score': final_score, 'total': total_questions})

    return render(request, 'exam/take_test.html', {
        'course': course,
        'video': video,
        'questions': questions
    })
