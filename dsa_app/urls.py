from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("interview", interview, name='interview'),
    path("contact-us", ContactView.as_view(), name='contact'),
    path("sheets", sheets,  name='sheets'),
    path("profile", profile, name='profile'),
    path("practice", practice, name='practice'),
    path('profile/<str:slug>', update_profile, name='update-profile'),
    path('question/<str:slug>', question_detail, name='question-detail'),
    path('sheet-detail/<str:slug>', sheet_detail, name='sheet-detail'),
    path('update-sheet/<str:slug>', update_sheet, name='update-sheet'),
    path('create-question', QuestionCreateView.as_view(), name='create-question'),
    path('update-question/<str:slug>', update_question, name='update-question'),
    path('delete-question/<str:slug>', delete_question, name='delete-question'),
    path('create-solution', SolutionCreateView.as_view(), name='create-solution'),
    path('solutions', solutions, name='solutions'),
    path("search-practice", search_practice, name='search-practice'),
    path("enroll/<str:slug>", enroll, name='enroll'),
    path("unenroll/<str:slug>", unenroll, name='unenroll'),
    path("mark-complete/<str:slug>", mark_completed, name='mark-complete'),
]
