from django.shortcuts import render

# Create your views here.
from robin_scraper.models import  Searcher
# from scraper_site.models import Book, Author, BookInstance, Genre
def index_not_used(request):
    # Render the HTML template index.html with the data in the context variable
    context = {
        'search_term': '',
    }
    return render(request, 'index.html', context=context)
    
def get_about(request):
    return render(request, 'about.html')

def index_used(request,search_term):
    #note that this will break if there is more than one Searcher Object
    #do model shenanigans to return 3 arrays and 5 metrics
    #Searcher.objects.get().display_consumer_key()
    context_categories = ['twitter_sentences','reddit_sentences','wikipedia_sentences','formal_confidence',\
                          'informal_confidence','twitter_metric','reddit_metric','wikipedia_metric','search_term']

    responses = Searcher.objects.get().return_all_goodies(search_term)
    context = dict(zip(context_categories,responses))
    # context = {  # data passed into template that the template displays
    #     'twitter_sentences': [x for x in range(10)],
    #     'reddit_sentences': [x for x in range(1,11)],
    #     'wikipedia_sentences': [x for x in range(2,12)],
    #     'formal_confidence': 'cheerio',
    #     'informal_confidence': 'nah',
    #     'twitter_metric': 10,
    #     'reddit_metric' : 100,
    #     'wikipedia_metric' : ,
    #     'search_term': search_term
    # }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# Create your views here.
