from django.contrib.auth import login, logout

from base.views import LoginRequiredMixin, AnonymousRequiredMixin, \
                       RedirectionMixin, TemplateView, FormView
from customer import models, forms

class Profile(LoginRequiredMixin, TemplateView):
    menu_item = 'profile'
    template_name = 'customer/profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        # Context
        data = super().get_context_data(**kwargs)
        data['orders'] = models.Order.objects.filter(profile__user=user)
        data['questions'] = models.Question.objects.filter(profile__user=user)
        return data

class Register(AnonymousRequiredMixin, RedirectionMixin, FormView):
    form_class = forms.Register

    template_name = 'customer/register.html'
    success_url = '/customer/register/complete/'

    def form_valid(self, form):
        form.create_profile(email_user=False)
        # Login after registration
        auth_user = form.validate_auth()
        if auth_user:
            login(self.request, auth_user)
        #
        return super().form_valid(form)

class RegisterComplete(LoginRequiredMixin, TemplateView):
    template_name = 'customer/register_complete.html'

class Login(AnonymousRequiredMixin, RedirectionMixin, FormView):
    form_class = forms.Login

    menu_item = 'login'
    template_name = 'customer/login.html'
    success_url = '/customer/' # redirect to profile page

    def form_valid(self, form):
        if form.auth_user:
            login(self.request, form.auth_user)
        #
        return super().form_valid(form)

class Logout(LoginRequiredMixin, TemplateView):
    menu_item = 'logout'
    template_name = 'customer/logout.html'

    def get_context_data(self, **kwargs):
        logout(self.request)
        return super().get_context_data(**kwargs)

class Hotline(FormView):
    form_class = forms.Hotline

    template_name = 'customer/hotline.html'
    success_url = '/customer/hotline/complete/'

    """
    def get_form_kwargs(self):
        '''
        Adds the request to the kwargs
        '''
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    """

    def form_valid(self, form):
        form.send(self.request)
        return super().form_valid(form)

class HotlineComplete(TemplateView):
    template_name = 'customer/hotline_complete.html'

class Question(LoginRequiredMixin, FormView):
    form_class = forms.Question

    template_name = 'customer/question.html'
    success_url = '/customer/question/complete/'

    def form_valid(self, form):
        form.send(self.request)
        return super().form_valid(form)

class QuestionComplete(LoginRequiredMixin, TemplateView):
    template_name = 'customer/question_complete.html'

class Order(LoginRequiredMixin, FormView):
    form_class = forms.Order

    template_name = 'customer/order.html'
    success_url = '/customer/'

    def form_valid(self, form):
        form.send(self.request)
        return super().form_valid(form)
