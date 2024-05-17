from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ranking_mark = models.IntegerField(default = 0)

class Category(models.Model):
    name = models.CharField(max_length= 100, unique = True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name.title()


class News_All(models.Model):

    link_Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    link_PostCategory = models.ManyToManyField(Category, through = "PostCategory")
    news = 'Нов'
    article = 'Ст'

    CHOICE_MAIN = [
        (news, 'Новости'),
        (article, 'Статья'),
    ]

    news_or_art = models.CharField(max_length=3,choices = CHOICE_MAIN, default = news)

    name = models.CharField(max_length= 100, unique = True)
    text = models.TextField(max_length= 100)
    time_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name.title()}"

    def get_absolute_url(self):
        return reverse('news_or_art_detail', args=[str(self.id)])

    def preview(self):
        if len(self.text) > 124:
            return f'{self.text[:124]}...'
        return self.text
    def title(self):
        if len(self.name) > 20:
            return f'{self.name[:20]}...'
        return self.name

#Связи для ManyToMany

class PostCategory(models.Model):
    #otm = OneToMany
    link_otm_Post_1 = models.ForeignKey(Category, on_delete=models.CASCADE)
    link_otm_Post_2 = models.ForeignKey(News_All, on_delete=models.CASCADE)



#---------------------------модель записи
# from datetime import datetime

class Appointment(models.Model):
    date = models.DateField(
        default = datetime.utcnow,
    )
    client_name = models.CharField(
        max_length = 200,
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}:{self.message}'
