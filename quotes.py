import random


def Quotes():
    quotes = [

        'Nie widzimy rzeczy takimi, jakie są. Widzimy je takimi, jakimi my jesteśmy.',

        'Życiowe wyzwania nie powinny Cię paraliżować. Powinny pomóc Ci odkryć, kim naprawdę jesteś. ',

        'Statek stojący w porcie jest bezpieczny, ale nie po to buduje się statki, by stały w portach. ',

        'Każdemu człowiekowi jest dany klucz do bram raju. Tym samym kluczem otwiera się bramy piekła. ',

        'Dobro jest dobrem, nawet gdy nikt go nie czyni. Zło jest złem, nawet gdy wszyscy je czynią. ',

        'W życiu każdego człowieka są dwa wielkie dni – pierwszy, w którym się rodzimy i drugi, w którym odkrywamy po co.',

        'stnieją dwa sposoby na łatwe prześliźnięcie się przez życie: wierzyć we wszystko lub wątpić we wszystko. Oba chronią nas przed samodzielnym myśleniem. '

    ]

    random_quote = random.choice(quotes)
    return random_quote
