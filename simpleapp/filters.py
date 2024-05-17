from django_filters import FilterSet, DateFilter #ModelChoiceFilter
from .models import News_All, Category
from django.forms import DateInput
# from .models import Material

class NewsFilter(FilterSet):
    time_in=DateFilter(
    field_name = 'time_in',
    widget = DateInput(attrs={'type':'date'}),
    label= 'Дата',
    lookup_expr = 'date__gte',
    )
    class Meta:
        model = News_All
        fields = {
            # 'productmaterial__material': ['exact'],
            'name': ['icontains'],
            'text': ['icontains'],
            # 'time_in': ['day__gt', 'month__gt', 'year__gt']

        }

#Фильтр для категорий
# class CategoryFilter(FilterSet):
#
#     class Meta:
#         model = Category
#         fields = {
#             # 'productmaterial__material': ['exact'],
#             'name': ['icontains'],
#             # 'time_in': ['day__gt', 'month__gt', 'year__gt']
#         }