from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter(original=0, test=0)
counter_click = Counter(original=0, test=0)


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    try:
        answer = request.GET['from-landing']
        if answer=='original':
            counter_click['original'] += 1
        else:
            counter_click['test'] += 1
    except KeyError:
        pass
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    answer = request.GET.get('ab-test-arg')
    if answer=='test':
        counter_show['test'] += 1
        return render(request, 'landing_alternate.html')
    else:
        counter_show['original'] += 1
        return render(request, 'landing.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:
    try:
        original_conversion = round(int(counter_click['original'])/int(counter_show['original']), 2)
    except ZeroDivisionError:
        original_conversion = 0
    try:
        test_conversion = round(int(counter_click['test'])/int(counter_show['test']), 2)
    except ZeroDivisionError:
        test_conversion = 0
    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
