from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView
from .models import *
from .forms import *
from django.db.models import Q
from django.db.models import Avg, Count


def home(request):
    basic = Question.objects.filter(level='BASIC')[:3]
    return render(request, "dsa_app/home.html", {'basic':basic})


def sheets(request):
    sheets = Sheet.objects.annotate(
        numbooks=Count('userquestion')
    )
    context = {
        'sheets': sheets
    }
    return render(request, "dsa_app/sheets.html", context)


@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user)
    sheet = Sheet.objects.get(user=user_profile)

    enrolled_sheets = Sheet.objects.filter(enrolled__user=request.user).annotate(
        numbooks=Count('userquestion')
    )

    questions = UserQuestion.objects.filter(sheet=sheet)
    context = {
        'profile': profile,
        'sheet': sheet,
        'questions': questions,
        'user_profile' :user_profile,
        'enrolled_sheets' : enrolled_sheets
    }
    return render(request, "dsa_app/profile/profile.html", context)


@login_required
def update_profile(request, slug):
    context = {}
    obj = get_object_or_404(UserProfile, uuid=slug)
    if request.method == 'POST':
        form = UpdateProfile(request.POST or None, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateProfile(instance=obj)
    context["form"] = form
    context["profile_user"] = obj.user
    return render(request, 'dsa_app/profile/update_profile.html', context)


def practice(request):
    basic = Question.objects.filter(level='BASIC')
    easy = Question.objects.filter(level='EASY')
    medium = Question.objects.filter(level='MEDIUM')
    hard = Question.objects.filter(level='HARD')
    expert = Question.objects.filter(level='EXPERT')
    context = {
        'basic': basic,
        'easy': easy,
        'medium': medium,
        'hard': hard,
        'expert': expert,
    }
    if request.user.is_authenticated:
        completed_questions = Question.objects.filter(is_solved__user=request.user)
        lst = []
        for ele in completed_questions:
            lst.append(ele.uuid)
            context['lst'] = lst

    return render(request, "dsa_app/practice.html", context)


def question_detail(request, slug):
    completed = False
    question = Question.objects.get(uuid=slug)
    user_profile = question.is_solved.filter(user=request.user)
    if user_profile and completed is not True:
        completed = True
    return render(request, 'dsa_app/question_detail.html', {'question':question, 'completed':completed})


@login_required
def sheet_detail(request, slug):
    context = {}
    sheet = Sheet.objects.get(uuid=slug)
    questions = UserQuestion.objects.filter(sheet=sheet)
    profile = UserProfile.objects.get(user=sheet.user.user)

    enrolled = False
    user_profile = sheet.enrolled.filter(user=request.user)

    if user_profile and enrolled is not True:
        enrolled = True

    context['sheet'] = sheet
    context['questions'] = questions
    context['profile'] = profile
    context['enrolled'] = enrolled
    return render(request, "dsa_app/sheets/sheet_detail.html", context)


@login_required
def update_sheet(request, slug):
    context = {}
    obj = get_object_or_404(Sheet, uuid=slug)
    if request.method == 'POST':
        form = UpdateSheetForm(request.POST or None, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('sheet-detail', slug=obj.uuid)
    else:
        form = UpdateSheetForm(instance=obj)

    context["form"] = form
    str_user = obj.user.user
    user = request.user
    context['sheet_user'] = str_user
    context['user'] = user
    return render(request, 'dsa_app/sheets/update_sheet.html', context)


class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    model = UserQuestion
    form_class = CreateQuestionForm
    template_name = 'dsa_app/questions/create_question.html'

    def get_success_url(self):
        return reverse('profile')

    def get_form_kwargs(self):
        kwargs = super(QuestionCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required
def update_question(request, slug):
    context = {}
    obj = get_object_or_404(UserQuestion, uuid=slug)
    if request.method == 'POST':
        form = UpdateQuestionForm(request.POST or None, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('sheet-detail', slug=obj.sheet.uuid)
    else:
        form = UpdateQuestionForm(instance=obj)

    context["form"] = form
    str_user = obj.sheet.user.user
    user = request.user
    context['question_user'] = str_user
    context['user'] = user
    return render(request, 'dsa_app/questions/update_question.html', context)


@login_required
def delete_question(request, slug):
    context = {}
    obj = get_object_or_404(UserQuestion, uuid=slug)
    if request.method == "POST":
        obj.delete()
        return redirect('sheet-detail', slug=obj.sheet.uuid)
    str_user = obj.sheet.user.user
    user = request.user
    context['question_user'] = str_user
    context['user'] = user
    return render(request, "dsa_app/questions/delete_question.html", context)


class SolutionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Solution
    form_class = CreateSolutionForm
    template_name = 'dsa_app/solutions/create_solution.html'

    def get_success_url(self):
        return reverse('profile')

    def get_form_kwargs(self):
        kwargs = super(SolutionCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@login_required
def solutions(request):
    solutions = Solution.objects.all()
    return render(request, 'dsa_app/solutions/solutions.html', {'solutions':solutions})


def search_practice(request):
    questions = Question.objects.all()
    query = request.GET.get('q')
    if query:
        questions = questions.filter(
            Q(name__icontains=query) |
            Q(Tags__icontains=query)
        ).distinct()

    context = {
        'questions': questions,
    }
    return render(request, "dsa_app/search_practice.html", context)


def enroll(request, slug):
    sheet = Sheet.objects.get(uuid=slug)
    user_profile = UserProfile.objects.get(user=request.user)
    sheet.enrolled.add(user_profile)
    return redirect('sheets')


def unenroll(request, slug):
    sheet = Sheet.objects.get(uuid=slug)
    user_profile = UserProfile.objects.get(user=request.user)
    sheet.enrolled.remove(user_profile)
    return redirect('sheets')


def mark_completed(request, slug):
    sheet = Question.objects.get(uuid=slug)
    user_profile = UserProfile.objects.get(user=request.user)
    sheet.is_solved.add(user_profile)
    return redirect('practice')