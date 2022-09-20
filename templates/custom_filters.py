from django import template

register = template.Library()

bad_words = ['редиска', 'мормышка', 'баран']

@register.filter()
def censor(in_text):
    if not isinstance(in_text, str):
        raise ValueError('Можно применить только к стоке!') # проверим, строка ли. Если строка, то в ней уже поищем плохие слова

    for word in bad_words:
        if word in bad_words:
            in_text = in_text.replace(word, f'{word[0]}{"*" * (len(word) - 1)}')
            return in_text

