from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import StudySession, Exam 
from .forms import KayitFormu, StudySessionForm, ExamForm

def register(request):
    if request.method == 'POST':
        form = KayitFormu(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = KayitFormu()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    study_form = StudySessionForm()
    exam_form = ExamForm()

    if request.method == 'POST':
        if 'add_study' in request.POST:
            study_form = StudySessionForm(request.POST)
            if study_form.is_valid():
                session = study_form.save(commit=False)
                session.user = request.user
                session.save()
                return redirect('dashboard')
        elif 'add_exam' in request.POST:
            exam_form = ExamForm(request.POST)
            if exam_form.is_valid():
                exam = exam_form.save(commit=False)
                exam.user = request.user
                exam.save()
                return redirect('dashboard')

   
    now = timezone.now()
    today = now.date()
    
   
    daily_tasks = StudySession.objects.filter(user=request.user, date__date=today).order_by('date')
    
   
    weekday = now.weekday()
    start_week = (now - timedelta(days=weekday)).replace(hour=0, minute=0, second=0, microsecond=0)
    start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    weekly_tasks = StudySession.objects.filter(user=request.user, date__gte=start_week).order_by('date')
    monthly_tasks = StudySession.objects.filter(user=request.user, date__gte=start_month).order_by('date')
    exams = Exam.objects.filter(user=request.user, date__gte=now).order_by('date')

    def calc_progress(tasks):
        total = tasks.count()
        done = tasks.filter(is_completed=True).count()
        return int((done / total) * 100) if total > 0 else 0

    last_7_days = []
    study_counts = []
    aylar = {"Jan": "Oca", "Feb": "Şub", "Mar": "Mar", "Apr": "Nis", "May": "May", "Jun": "Haz", "Jul": "Tem", "Aug": "Ağu", "Sep": "Eyl", "Oct": "Eki", "Nov": "Kas", "Dec": "Ara"}

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        eng_date = day.strftime('%d %b')
        tr_date = eng_date
        for eng, tr in aylar.items():
            if eng in eng_date:
                tr_date = eng_date.replace(eng, tr)
                break
        last_7_days.append(tr_date)
        count = StudySession.objects.filter(user=request.user, date__date=day, is_completed=True).count()
        study_counts.append(count)

    context = {
        'form': study_form, 'exam_form': exam_form,
        'daily_tasks': daily_tasks, 'weekly_tasks': weekly_tasks, 'monthly_tasks': monthly_tasks,
        'exams': exams, 'daily_progress': calc_progress(daily_tasks), 'weekly_progress': calc_progress(weekly_tasks),
        'monthly_progress': calc_progress(monthly_tasks), 'chart_labels': last_7_days, 'chart_data': study_counts,
    }
    return render(request, 'dashboard.html', context)

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(StudySession, id=task_id, user=request.user)
    task.is_completed = not task.is_completed 
    task.save()
    return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    
    task = get_object_or_404(StudySession, id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')
