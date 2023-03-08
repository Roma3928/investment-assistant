from django.contrib import admin
from core.models import CompanyCategory, Company, Promotion, Tax


admin.site.register(CompanyCategory)
admin.site.register(Company)
admin.site.register(Promotion)
admin.site.register(Tax)
