from django.urls import path

from forum.views import *
from forum.models import *

urlpatterns = [
    path('form', FeedView.as_view(), name='main'),
    path('hot', HotQuestionsView.as_view(), name='hot'),
    path('ask', AskView.as_view(), name='ask'),
    path('question/<pk>', QuestionView.as_view(), name='question'),

    path('tag/<str:tag_name>', TagQuestionView.as_view(), name='tag'),
    path('question/<pk>/like', VotesView.as_view(model=Question, vote=LikeDislike.LIKE)),
    path('question/<pk>/dislike', VotesView.as_view(model=Question, vote=LikeDislike.DISLIKE)),
    path('answer/<pk>/like', VotesView.as_view(model=Answer, vote=LikeDislike.LIKE)),
    path('answer/<pk>/dislike', VotesView.as_view(model=Answer, vote=LikeDislike.DISLIKE)),
    path('question/<pk>/isliked', IsLikedView.as_view(model=Question)),
    path('answer/<pk>/isliked', IsLikedView.as_view(model=Answer)),
]
