from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

#from django.http import Http404
#from django.core.urlresolvers import reverse_lazy
#from django.utils.translation import ugettext_lazy as _

class LoginRequiredMixin(object):
    '''
    Mixin for login protection
    '''
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class AnonymousRequiredMixin(object):
    '''
    Mixin for views that checks that the user is NOT logged in, redirecting to
    the profile page if necessary
    '''
    def dispatch(self, request, *args, **kwargs):
        if request.user is not None and request.user.is_authenticated():
            # Redirects to the profile page
            return HttpResponseRedirect('/customer/')
        return super().dispatch(request, *args, **kwargs)

class RedirectionMixin(object):
    '''
    Mixin which changes success_url to "next" GET parameter of the form
    '''
    success_url = None

    def get_success_url(self):
        return self._next_url(default=self.success_url)

    def get_context_data(self, **kwargs):
        # Context
        data = super().get_context_data(**kwargs)
        data['next'] = self._next_url()
        return data

    def _next_url(self, default=None):
        return self.request.GET.get('next', default)

class MenuMixin(object):
    '''
    Mixin which adds menu to the view
    '''
    menu_item = None # name of menu item of the view

    def get_context_data(self, **kwargs):
        # Info menu section
        menu_info = [('news', 'Новости'),
                     ('specoffers', 'Спецпредложения'),
                     ('services', 'Услуги', 'page'),
                     ('papers', 'Документы'),
                     ('about', 'О компании', 'page')]
        # Customer menu section
        user = self.request.user
        if user.is_authenticated():
            menu_customer = [('profile', user.first_name),
                             ('logout', 'Выйти')]
        else:
            menu_customer = [('login', 'Войти')]
        # Context
        data = super().get_context_data(**kwargs)
        data['index'] = self._item_struct('home', 'Cargo Trek')
        data['menu'] = {
            'info': (self._item_struct(*item) for item in menu_info),
            'customer': (self._item_struct(*item) for item in menu_customer)
        }
        data['menu_item'] = self.menu_item # current menu item
        return data

    def _item_struct(self, name, text, path=''):
        '''
        Structure of a menu item in the form of dictionary
        '''
        return {'name': name, 'text': text, 'path': path}

class TemplateView(MenuMixin, generic.TemplateView):
    pass

class ListView(MenuMixin, generic.ListView):
    pass

class DetailView(MenuMixin, generic.DetailView):
    pass

class FormView(MenuMixin, generic.edit.FormView):
    pass
