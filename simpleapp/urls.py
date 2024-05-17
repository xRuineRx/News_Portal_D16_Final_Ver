from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, AppointmentView, \
    CategoryListView, subscribe  # ,create_product
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
#Кэш добавлен для всех новостей!

# app_name="appointments"

urlpatterns = [
    path('News_all', cache_page(60)(PostList.as_view()), name='news_list'),
    path('News_all/<int:id>', cache_page(100)(PostDetail.as_view()), name= 'news_or_art_detail'),
    path('create_news/', NewsCreate.as_view(), name= 'create_news'),
    path('art/create_news/', NewsCreate.as_view(), name= 'create_art'),
    path('news_or_art/update/<int:pk>/', NewsUpdate.as_view(), name='news_update'),
    path('news_or_art/delete/<int:pk>/', NewsDelete.as_view(), name='news_delete'),
    path('make_appointment/', AppointmentView.as_view(), name='make_appointment'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name = 'subscribe')
]