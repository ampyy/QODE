from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class UpdateProfile(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'whats your name coder?'}),
                           label='Name')
    profile_picture = forms.ImageField()
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'where you live coder?'}),
                               label='Location')
    about_yourself = forms.TextInput()
    profession = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'what you do coder?'}),
                                 label='Profession', required=False)
    instagram_link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'insta profile link?'}),
                                     label='Instagram Link', required=False)
    linkedin_link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'linkedin profile link?'}),
                                    label='Linkedin Link', required=False)
    github_link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'github profile link?'}),
                                  label='Github Link', required=False)
    portfolio_link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'your own portfolio link if have?'}),
                                     label='Portfolio Link', required=False)

    class Meta:
        model = UserProfile
        fields = ('name', 'profile_picture', 'location', 'about_yourself', 'profession',
                  'instagram_link', 'linkedin_link', 'github_link', 'portfolio_link')


class UpdateSheetForm(forms.ModelForm):
        name = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': 'Your Sheet Name'}),
            label='Sheet Name')
        description = RichTextField()

        class Meta:
            model = Sheet
            fields = ('name', 'description',)


class CreateQuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreateQuestionForm, self).__init__(*args, **kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        self.fields['sheet'].queryset = Sheet.objects.filter(
            user=user_profile)

    sheet = forms.ModelChoiceField(queryset=None, initial=0)
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'question Name'}),
        label='Question Name')
    question_link = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'your question link'}),
        label='Question link')
    solution_link = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'your solution link'}),
        label='Solution link')

    class Meta:
        model = UserQuestion
        fields = ('sheet', 'name', 'question_link', 'solution_link')


class CreateSolutionForm(forms.ModelForm):
    question = forms.ModelChoiceField(queryset=Question.objects.all())
    solution = RichTextField()

    class Meta:
        model = Solution
        fields = ('question', 'solution',)


class UpdateQuestionForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'question Name'}),
        label='Question Name')
    question_link = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'your question link'}),
        label='Question link')
    solution_link = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'your solution link'}),
        label='Solution link')

    class Meta:
        model = UserQuestion
        fields = ('name', 'question_link', 'solution_link',)