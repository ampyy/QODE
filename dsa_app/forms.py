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
        description = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': 'Your Sheet Description'}),
            label='Sheet Description')

        class Meta:
            model = Sheet
            fields = ('name', 'description',)


TOPIC = (
    ('---Choose---', '---choose---'),
    ('Array', 'Array'),
    ('String', 'String'),
    ('LinkedList', 'LinkedList'),
    ('Stack', 'Stack'),
    ('Queue', 'Queue'),
    ('Tree', 'Tree'),
    ('BST', 'BST'),
    ('Graph', 'Graph'),
    ('Heap', 'Heap'),
    ('Sorting', 'Sorting'),
    ('Searching', 'Searching'),
    ('Greedy', 'Greedy'),
    ('DP', 'Dynamic Programming'),
    ('Backtracking', 'Backtracking'),
)


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
    Tag =  forms.ChoiceField(choices = TOPIC)
    question_link = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'your question link'}),
        label='Question link')
    solution_link = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'your solution link'}),
        label='Solution link')

    class Meta:
        model = UserQuestion
        fields = ('sheet', 'name', 'Tag', 'question_link', 'solution_link')


class CreateSolutionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreateSolutionForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = UserProfile.objects.filter(
            user=self.request.user)

    user = forms.ModelChoiceField(queryset=None, initial=0)
    question = forms.ModelChoiceField(queryset=Question.objects.all())
    solution_file = forms.FileField(label="Your solution file (1Mb-2Mb)")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Explain Solution (Optional)'}),
        label='Description')

    class Meta:
        model = Solution
        fields = ('user', 'question', 'solution_file', 'description')


class UpdateQuestionForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'question Name'}),
        label='Question Name')
    Tag = forms.ChoiceField(choices=TOPIC)
    question_link = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'your question link'}),
        label='Question link')
    solution_link = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'your solution link'}),
        label='Solution link')

    class Meta:
        model = UserQuestion
        fields = ('name', 'Tag', 'question_link', 'solution_link',)


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'your name?'}),
        label='Name')
    email_id = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'email?'}),
        label='Email')
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'what is your query?'}),
        label='Query')

    class Meta:
        model = Contact
        fields = ('name', 'email_id', 'description',)