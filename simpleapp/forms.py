from django import forms
from django.core.exceptions import ValidationError
from .models import  News_All, Category


class NewsForm(forms.ModelForm):
    class Meta:
        model = News_All
        fields = [
            'name',
            'text',
            'link_PostCategory',
        ]
    # def clean(self):
    #     cleaned_data = super().clean()
    #     description = cleaned_data.get("description")
    #     if description is not None and len(description)< 20:
    #         raise ValidationError({
    #             "description": "Описание не может быть меньше 20 символов."
    #         })
    #
    #     name = cleaned_data.get("name")
    #     if name == description:
    #         raise ValidationError({
    #             #"name": "Описание не должно быть индетичным названию"
    #             "Описание не должно быть индетичным названию"
    #         })
    #
    #     return cleaned_data

    # Вариант валидации 2

    # class ProductForm(forms.ModelForm):
    #     Тоже самое что и выше, с разницей что описание ограничиваем по другому и не можем
    #     Проводить совместную проверку полей текста в названии и описании
    #     description = forms.CharField(min_length=20)
    #
    #     class Meta:
    #         model = Product
    #         fields = [
    #             'name',
    #             'description',
    #             'category',
    #             'price',
    #             'quantity',
    #         ]
    #
    #     def clean(self):
    #         cleaned_data = super().clean()
    #         name = cleaned_data.get("name")
    #         description = cleaned_data.get("description")
    #
    #         if name == description:
    #             raise ValidationError(
    #                 "Описание не должно быть идентичным названию."
    #             )
    #
            # return cleaned_data


    # Вариант валидации 3 через функцию проверки
    #Обрати внимание на sеlf.cleaned_data

    # class ProductForm(forms.ModelForm):
    #     class Meta:
    #         model = Product
    #         fields = [
    #             'name',
    #             'description',
    #             'category',
    #             'price',
    #             'quantity',
    #         ]
    #
    #     def clean_name(self):
    #         name = self.cleaned_data["name"]
    #         if name[0].islower():
    #             raise ValidationError(
    #                 "Название должно начинаться с заглавной буквы."
    #             )
    #         return name