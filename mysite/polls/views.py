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
    context_object_name = 'latest_polls_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        #Add additional data
        #context['testtext'] = "Test text! It works!!"
        return context
	
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        #return Pollset.objects.filter(
        #    pub_date__lte=timezone.now()
        #).order_by('-pub_date')[:5]
        return Pollset.objects.filter(
            is_active=True
        ).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixinSpecial,generic.DetailView):
    
    model = Pollset
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
		#Extra content
        #context['testtext'] = "Test text! It works!!"
        return context
	
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        #obj = Pollset.objects.filter(pub_date__lte=timezone.now())
        obj = Pollset.objects.filter(is_active=True)
        #for k in obj:
        #    print(k.user_performed.all())
        return obj

class ResultsView(PermissionRequiredMixinSpecial,generic.DetailView):
    model = Pollset
    permission_required = 'polls.view_choice'
    template_name = 'polls/results.html'
    raise_exception = True
    permission_denied_message = 'No permission authorization'
    pollset = get_object_or_404(Pollset, pk=pk)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        #questions_obj_list = pollset.objects.question_set.all()
        return context

	

@login_required
def vote(request, pollset_id):
    pollset = get_object_or_404(Pollset, pk=pollset_id)
	
    questions_obj_list = pollset.question_set.all()
    try:
        #selected_choice = pollset.question_set.get(pk=request.POST["question%s"%])
        selected_choices = {}
        for question in questions_obj_list:
            #selected_choices.append(pollset.question_set.get(pk=request.POST["question%s"%question.id]))
            pk = request.POST["choice%s"%question.id]
            #print("question.id ",question.id)
            #print("pk ",pk)
            selected_choices[question.id] = pk
            #print("question%s"%question.id)
        selected_choices_obj = Choice.objects.filter(pk__in=[v for (k,v) in selected_choices.items()])
        #return HttpResponse([v for (k,v) in selected_choices.items()]) 
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a choice.")
        return HttpResponseRedirect(reverse('polls:detail',kwargs={'pk':pollset_id}))
        #context = {'pollset': pollset}
        #return render(request, 'polls/detail.html' , context)
    else:
        usr = request.user
        if usr.has_perm('polls.add_choice'):
            if usr not in pollset.user_performed.all():
                for choice in selected_choices_obj:
                    choice.votes += 1
                    choice.save()
                pollset.user_performed.add(usr)
                return HttpResponseRedirect(reverse('polls:results', args=(pollset.id,)))
            else:
                messages.error(request, 'You have already voted!')
                return HttpResponseRedirect(reverse('polls:detail',kwargs={'pk':pollset.id}))
        else:
            messages.error(request, "You don't have permission to vote.... ")
            return HttpResponseRedirect(reverse('polls:detail',kwargs={'pk':pollset.id}))
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
        

@login_required
def testout(request):
    #question = get_object_or_404(Question, pk=pollset_id)

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
		
		