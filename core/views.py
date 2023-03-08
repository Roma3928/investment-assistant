from django.shortcuts import render
from django.views.generic import ListView, DetailView
from news.models import News
from core.models import Promotion, Tax, Company


def index(request):
    content = News.objects.all()
    context = {
        'content': content,
    }
    return render(request, 'index.html', context=context)


class TaxView(ListView):
    model = Tax
    ordering = ["state"]
    template_name = "core/tax.html"
    context_object_name = 'tax'


class PromotionListView(ListView):
    model = Promotion
    template_name = 'core/analytics.html'

    def get_queryset(self):
        exchange = self.request.GET.get('exchange', 'Московская биржа')  # СПб биржа
        return Promotion.objects.filter(company__exchange=exchange)


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'core/company_details.html'
    slug_field = 'symbol'
    slug_url_kwarg = 'symbol'
