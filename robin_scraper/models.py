from django.db import models

from django.urls import reverse  # Used to generate URLs by reversing the URL patterns

from . import z_scraper

class Searcher(models.Model):
    t_consumer_key =models.CharField(max_length=200)
    t_consumer_secret =models.CharField(max_length=200)
    t_access_token =models.CharField(max_length=200)
    t_access_secret =models.CharField(max_length=200)
    r_client_id =models.CharField(max_length=200)
    r_client_secret =models.CharField(max_length=200)
    r_username =models.CharField(max_length=200)
    r_password =models.CharField(max_length=200)

    def return_all_goodies(self,phrase):
        #['twitter_sentences','reddit_sentences','wikipedia_sentences','formal_confidence',\
        #                  'informal_confidence','twitter_metric','reddit_metric','wikipedia_metric','search_term']
        twitt_api = z_scraper.twitter_api_and_cleaner(phrase,self)
        reddit_api = z_scraper.reddit_api_and_cleaner(phrase,self)
        wiki_api = z_scraper.wikipedia_api_and_cleaner(phrase,self)

        twitterResults, twitterConf, avgRT = twitt_api.search(50, 10, 5, 10)
        redditResults, redditConf, avgUV = reddit_api.search(50, 60, 5, 10)
        wikiResults, wikiConf, meaninglessMetric = wiki_api.search(10, 2, 1, 10)

        return [twitterResults,redditResults,wikiResults,"dna","dna2","{:.2f}".format(avgRT),"{:.2f}".format(avgUV),meaninglessMetric,phrase]
    def __str__(self):
        """String for representing the Model object."""
        return self.r_client_id

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_consumer_key(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return self.t_consumer_key





# Create your models here.
