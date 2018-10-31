from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages

from .models import Pollset, Choice, Question

class LoginRequiredMixinSpecial(LoginRequiredMixin):
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'You should log in first')
        return super(LoginRequiredMixinSpecial, self).handle_no_permission()
		
class PermissionRequiredMixinSpecial(PermissionRequiredMixin):
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, "You don't have permission to view this page. Please log in")
        return HttpResponseRedirect(super(ResultsView, self).get_login_url())

class IndexView(LoginRequiredMixinSpecial,generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['testtext'] = "Test text! It works!!"
        return context
	
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixinSpecial,generic.DetailView):
    
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['testtext'] = "Test text! It works!!"
        return context
	
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        obj = Question.objects.filter(pub_date__lte=timezone.now())
        for k in obj:
            print(k.user_performed.all())
        return obj

class ResultsView(PermissionRequiredMixinSpecial,generic.DetailView):
    model = Question
    permission_required = 'polls.view_choice'
    template_name = 'polls/results.html'
    raise_exception = True
    permission_denied_message = 'No permission authorization'

	

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        choice_num = question.choice_set.get(pk=request.POST['choice'])
        #print('choice = ',request.POST['choice'])
        #print("User voted - ", request.user in question.user_performed.all())
        #print("User voted - ", request.user.has_perm('polls.view_choice'))
        #try:
        #    usr = request.user
        #except (TypeError):
        #    return render(request, 'polls/detail.html', {
        #        'question': question,
        #        'error_message': "You should login first",
        #    })
        usr = request.user
        if usr.has_perm('polls.add_choice'):
            if usr not in question.user_performed.all():
                selected_choice.votes += 1
                selected_choice.save()
                question.user_performed.add(usr)
                print('success')
            else:
                #return render(request, 'polls/detail.html', {
                #    'question': question,
                #    'error_message': "You have already voted",
                #})
                messages.error(request, 'You have already voted - MESSAGE')
                return HttpResponseRedirect(reverse('polls:detail',kwargs={'pk':question.id}))
        else:
            #return render(request, 'polls/detail.html', {
            #    'question': question,
            #    'error_message': "You don't have permission to vote",
            #})
            #HttpResponse(reverse('polls:detail', args=(question.id,)))
            messages.error(request, "You don't have permission to vote")
            return HttpResponseRedirect(reverse('polls:detail',kwargs={'pk':question.id}))
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def testout(request):
    #question = get_object_or_404(Question, pk=question_id)

    #return HttpResponse("the answer is %s" % request.user.is_authenticated())

	email = EmailMessage(
	    'Hello',
	    'Body goes here',
	    'anton.tushev@primetals.com',
	    ['anton.tushev@primetals.com'],
	    [],
	    reply_to=['anton.tushev@primetals.com'],
	    headers={'Message-ID': 'foo'},
	)
	email.send()
	
	return HttpResponse(request.user.has_perm('polls.view_choice'))
		
		