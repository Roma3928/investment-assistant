from annoying.functions import get_object_or_None
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView

from forum.forms import AnswerForm, NewQuestionForm
from forum.models import Question, Answer, Tag, LikeDislike


class FeedView(ListView):
    paginate_by = 6
    model = Question
    ordering = ["-date"]
    template_name = "forum/feed.html"


class QuestionView(DetailView):
    model = Question
    template_name = "forum/question.html"
    form_class = AnswerForm

    def get_context_data(self, **kwargs):
        return super(QuestionView, self).get_context_data(form=self.form_class, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.object = self.get_object()
        context = self.get_context_data()
        form = self.form_class(request.POST)
        if form.is_valid():
            Answer.objects.create(author=request.user,
                                  text=form.cleaned_data['text'],
                                  question=self.object)
            return self.render_to_response(context)
        else:
            context['form'] = form
            return self.render_to_response(context)


class HotQuestionsView(ListView):
    paginate_by = 6
    model = Question
    ordering = ["-rate"]
    template_name = "forum/feed.html"


class TagQuestionView(ListView):
    paginate_by = 6
    template_name = "forum/tag_questions.html"
    context_object_name = "questions"

    def get_context_data(self, **kwargs):
        kwargs["tag"] = self.kwargs["tag_name"]
        return super(TagQuestionView, self).get_context_data(**kwargs)

    def get_queryset(self):
        return Tag.objects.questions_by_tag(self.kwargs['tag_name'])


class AskView(LoginRequiredMixin, FormView):
    form_class = NewQuestionForm
    template_name = 'forum/ask.html'
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            question = Question.objects.create(author=request.user,
                                               title=form.cleaned_data['title'],
                                               text=form.cleaned_data['text'])
            form.cleaned_data['tags'].strip()
            for tagTitle in form.cleaned_data['tags'].split():
                tag = Tag.objects.get_or_create(title=tagTitle)[0]
                question.tags.add(tag)
                question.save()
            return HttpResponseRedirect(reverse('question', args=[question.pk]))
        else:
            return self.form_invalid(form)


class VotesView(LoginRequiredMixin, View):
    login_url = 'login'
    model = None
    vote = None

    def post(self, request, pk):
        color = None
        if self.vote == LikeDislike.LIKE:
            color = 'green'
        else:
            color = 'red'
        obj = self.model.objects.get(pk=pk)
        vote_obj = get_object_or_None(LikeDislike, content_type=ContentType.objects.get_for_model(obj),
                                      object_id=pk,
                                      user=request.user)
        if not vote_obj:
            new = LikeDislike(vote=self.vote, user=request.user,
                              content_object=obj)
            new.save()
            new.content_object.rate += self.vote
            new.content_object.save()

            return JsonResponse({'rate': new.content_object.rate, 'color': color})
        if vote_obj.vote == self.vote:
            return JsonResponse({'rate': vote_obj.content_object.rate, 'color': color})
        else:
            vote_obj.delete()
            return JsonResponse({'rate': vote_obj.content_object.rate, 'color': 'black'})


class IsLikedView(LoginRequiredMixin, View):
    login_url = 'login'
    model = None

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        vote_obj = get_object_or_None(LikeDislike, content_type=ContentType.objects.get_for_model(obj),
                                      object_id=pk,
                                      user=request.user)
        if not vote_obj:
            return JsonResponse({'isliked': 0})
        if vote_obj.vote == 1:
            return JsonResponse({'isliked': 1})
        else:
            return JsonResponse({'isliked': -1})
