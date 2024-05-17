from django import template

register = template.Library()

CURRENCIES_SYMBOLS ={
    'rub': 'P',
    'usd': '$',
}

@register.filter()
def currency(value, code = 'rub'):
    postfix = CURRENCIES_SYMBOLS[code]
    return f'{value}{postfix}'

censor_list = [ "Редиска", "редиска"]

@register.filter()
def censor(text):
    try:
        for word in censor_list:
            text = text.replace(word[1:], '*'*len(word[1:]))
        return text
    except AttributeError:
        return "Применять функцию исключительно к тексту !"
    except Exception:
        return "Какая то иная ошибка >_<"

