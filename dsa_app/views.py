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
    questions = UserQuestion.objects.filter(sheet=sheet)
    context = {
        'profile': profile,
        'sheet': sheet,
        'questions': questions,
        'user_profile' :user_profile
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
    context  = {
        'basic' : basic,
        'easy' : easy,
        'medium' : medium,
        'hard' :hard,
        'expert' : expert
    }
    return render(request, "dsa_app/practice.html", context)


def question_detail(request, slug):
    question = Question.objects.get(uuid=slug)
    return render(request, 'dsa_app/question_detail.html', {'question':question})


@login_required
def sheet_detail(request, slug):
    context = {}
    sheet = Sheet.objects.get(uuid=slug)
    questions = UserQuestion.objects.filter(sheet=sheet)
    profile = UserProfile.objects.get(user=sheet.user.user)
    context['sheet'] = sheet
    context['questions'] = questions
    context['profile'] = profile
    return render(request, "dsa_app/sheets/sheet_detail.html", context)


@login_required
def update_sheet(request, slug):
    context = {}
    obj = get_object_or_404(Sheet, uuid=slug)
    if request.method == 'POST':
        form = UpdateSheetForm(request.POST or None, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('profile')
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
            return redirect('profile')
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
        return redirect('profile')
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


@login_required
def solutions(request):
    solutions = Solution.objects.all()
    return render(request, 'dsa_app/solutions/solutions.html', {'solutions':solutions})

