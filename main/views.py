from django.views.generic import TemplateView
from .models import *

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['directions'] = Direction.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        direction_id = request.POST.get('direction')
        birth_date = request.POST.get('birth_date')

        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            direction_id=direction_id,
            birth_date=birth_date
        )

        direction = Direction.objects.get(id=direction_id)

        subjects = [
            (direction.subject1, direction.count1),
            (direction.subject2, direction.count2),
            (direction.subject3, direction.count3),
        ]

        for subject, count in subjects:
            questions = Question.objects.filter(subject=subject).order_by('?')[:count]
            for q in questions:
                StudentAnswer.objects.create(student=student, question=q)
                

        return redirect('quiz', student_id=student.id)


from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse

def quiz(request, student_id):

    if request.method == 'POST':
        print(request.POST)

        student_question_id = request.POST['student_question_id']
        answer_id = request.POST['answer_id']

        student_question = StudentAnswer.objects.get(id=student_question_id)
        student_question.answer_id = answer_id
        student_question.save()

        return redirect('quiz', student_id=student_id)

    student_question = StudentAnswer.objects.filter(student_id=student_id, answer__isnull=True).first()

    if student_question is None:

        student = Student.objects.get(id=student_id)

        subject1 = student.direction.subject1
        subject2 = student.direction.subject2
        subject3 = student.direction.subject3

        point1 = student.direction.point1
        point2 = student.direction.point2
        point3 = student.direction.point3

        st_answer = StudentAnswer.objects.filter(student_id=student_id, answer__is_correct=True)

        sub1 = st_answer.filter(question__subject=subject1).count()
        sub2 = st_answer.filter(question__subject=subject2).count()
        sub3 = st_answer.filter(question__subject=subject3).count()

        return render(request, 'result.html', 
                      {
                          "student":student,
                          "subject1":subject1,
                          "subject2":subject2,
                          "subject3":subject3,
                          "count1":sub1,
                          "count2":sub2,
                          "count3":sub3,
                          "score1":sub1*point1,
                          "score2":sub2*point2,
                          "score3":sub3*point3,
                          "result":round((sub1*point1 + sub2*point2 + sub3*point3), 2),
                      }
                      )

    data = {
        'student_id':student_id,
        'student_question_id':student_question.id,
        'question':student_question.question,
        'answers':Answer.objects.filter(question=student_question.question),
    }

    return render(request, 'quiz.html', data)