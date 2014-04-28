from django.http import Http404
#from django.utils.translation import ugettext_lazy as _

from datetime import datetime
from itertools import chain
from operator import attrgetter

from base.views import TemplateView, ListView, DetailView
from info import models

class Home(TemplateView):
    menu_item = 'home'
    template_name = 'info/home.html'

    ads_count = 6 # number of latest news and special offers

    def get_context_data(self, **kwargs):
        n = self.ads_count
        news_list = models.News.objects.extra(select={'tag': '"news"'})[:n]
        specoffers_list = \
            models.SpecOffer.objects.filter(finished=False) \
                                    .extra(select={'tag': '"specoffer"'})[:n]
        # Ads -- news and special offers
        ads = sorted(chain(news_list, specoffers_list),
                     key=attrgetter('created_at'), reverse=True)
        # Context
        data = super().get_context_data(**kwargs)
        data['last_ads'] = ads[:n] # latest news and special offers
        return data

class News(ListView):
    '''
    List of all news filtered by year
    '''
    menu_item = 'news'
    template_name = 'info/news.html'
    context_object_name = 'news_list' # name of the list in template
    #paginate_by = 10 # number of news on one page

    years = [] # list of available years
    year = None # filter

    def get_queryset(self):
        # Available datetimes
        dt_qset = models.News.objects.datetimes('created_at', 'year',
                                                order='DESC')
        self.years = [dt.year for dt in dt_qset]
        #
        if 'year' in self.kwargs:
            try:
                self.year = int(self.kwargs['year'])
            except ValueError:
                raise Http404()
        else:
            self.year = self.years[0] # last available year
        #
        return models.News.objects.filter(created_at__year=self.year)

    def get_context_data(self, **kwargs):
        # Context
        data = super().get_context_data(**kwargs)
        data['year'] = self.year # year of displayed news
        data['years'] = self.years # available years of all news
        return data

class SpecOffers(ListView):
    '''
    List of all special offers filtered by state
    '''
    menu_item = 'specoffers'
    template_name = 'info/specoffers.html'
    context_object_name = 'specoffers_list' # name of the list in template
    #paginate_by = 10 # number of special offers on one page

    state = 'active' # filter, active by default

    def get_queryset(self):
        # Available filters
        manager = models.SpecOffer.objects
        qset_by_state = {
            'active': (lambda: manager.filter(finished=False)),
            'finished': (lambda: manager.filter(finished=True)),
            'all': manager.all
        }
        # Current filter
        if 'state' in self.kwargs:
            self.state = self.kwargs['state']
        # Fetches special offers
        if self.state not in qset_by_state:
            raise Http404()
        return qset_by_state[self.state]()

    def get_context_data(self, **kwargs):
        # States menu section
        menu_states = [('active', 'действующие'),
                       ('finished', 'завершенные'),
                       ('all', 'все')]
        # Context
        data = super().get_context_data(**kwargs)
        menu = data.get('menu', {})
        menu.update({'states': ({'name': name, 'text': text}
                                for (name, text) in menu_states)})
        data['menu'] = menu # all main menus + states menu
        data['state'] = self.state # current state
        return data

class Page(DetailView):
    model = models.Page
    slug_field = 'name'

    template_name = 'info/page.html'
    context_object_name = 'page' # name of the object in template

    def get_object(self, queryset=None):
        if 'slug' in self.kwargs:
            self.menu_item = self.kwargs['slug']
        #
        if not self.menu_item:
            raise Http404()
        #
        return super().get_object(queryset)

class Papers(TemplateView):
    menu_item = 'papers'
    template_name = 'info/papers.html'
