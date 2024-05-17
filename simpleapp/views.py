from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import  News_All, Category
from datetime import datetime
from .filters import  NewsFilter
from .forms import  NewsForm
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .models import Appointment

#Для Логирования
# import logging
#
# logger = logging.getLogger(__name__)

# Create your views here.
class PostList(ListView):
    model = News_All
    ordering = '-time_in'

    template_name = 'flatpages/News_all.html'
    context_object_name = 'news'

    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = News_All
    pk_url_kwarg = 'id'

    template_name = 'flatpages/News_all_post.html'
    context_object_name = "news"

#Создание обновление и удаление новостей/статей

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_news_all',)
    form_class = NewsForm
    model = News_All
    template_name = 'flatpages/News_all_create_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news_or_art/art/create_news/':
            post.news_or_art = 'Ст'
        post.link_Author = self.request.user.author
        post.save()
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_news_all',)
    form_class = NewsForm
    model = News_All
    template_name = 'flatpages/News_all_create_news.html'



class NewsDelete(DeleteView):
    model = News_All
    template_name = 'flatpages/news_delete.html'
    success_url = reverse_lazy('news_list')


#-----------------Представление для почты и БД
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from .models import Appointment
from django.template.loader import render_to_string
from django.conf import settings


class AppointmentView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'flatpages/make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date = datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name = request.POST['client_name'],
            message = request.POST['message'],
        )
        appointment.save()

        html_content = render_to_string(
            'flatpages/appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        #первоначальный_шаблон
        # send_mail(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%m %d")}',
        #     message=appointment.message,
        #     from_email='МОЯ_ПОЧТА@yandex.ru',
        #     recipient_list=[]
        # )

        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%m-%d")}',
            body=appointment.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['ilyas.mahashev.lesnic@mail.ru',]
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('appointments:make_appointment')

class CategoryListView(ListView):
    model = News_All
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.link_PostCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = News_All.objects.filter(link_PostCategory=self.link_PostCategory).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.link_PostCategory.subscribers.all()
        context['category'] = self.link_PostCategory
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категорий'
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message' : message})



