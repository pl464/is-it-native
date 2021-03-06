# Is It Native
Website: [link](https://is-it-native.herokuapp.com/robin/)
## Function and Purpose
This webpage is intended to help English learners. This tool allows users to search up an English string - perhaps words or phrases they’ve encountered or come up with themselves- and see how it’s used on various web sources. This can not only provide examples for the word or phrase, but also determine whether it’s likely to be used at all. 
            <br><br>
            The tool also offers a prediction as to how likely the string is to appear in native English by using metrics obtained from the data, such as retweets and upvotes. The reasoning is that words or phrases used in native-approved contexts are more likely to be popular/retweeted/upvoted, and so these metrics can be used to indicate native language. Though this is obviously oversimplified, we’ve found that the predictions hold water a surprising amount of the time (see “Documentation” for some examples). Currently, the prediction about “informal contexts” involves retweets and upvotes, while the one for “formal contexts” only involves the number of hits from Wikipedia. In the future, we could expand to include more sources.<br><br>
## Implications
Undoubtedly, since the results consist of literal matches for the input string, there will be scenarios in which the words/phrases appear in different contexts. And since we’re scraping data from social media sites like Twitter or Reddit, the results may not be examples of grammatical English taught in schools. Yet these are “messy” conditions in which natural language is acquired. Words or phrases <em>do</em> appear in different contexts, and native language often <em>does</em> deviate from prescribed grammar rules. The user simply takes in the results as they appear, and makes their own interpretations- much like how a child, for example, might learn colloquial language. This is how we justify the results as having language-learning value: because the feedback is not necessarily straightforward, the results adhere towards a more natural model of language-learning (which is usually not a straightforward process).
            <br><br>
            One more thing to note is that the results are the most recent matches from these sites. This works out nicely for ensuring that the results include the most up-to-date contexts, which is important for a language as dynamic as English. Something that doesn’t work out as nicely is that if the input string is <em>really popular</em>, the most recent results might not have many retweets/upvotes- which could increase the likelihood of an inaccurate prediction. 
            <br><br>
## Technologies Used
The program to retrieve and process the data is written in Python. To scrape the data, we used the Python libraries Twython, Praw, and BeautifulSoup to access the Twitter, Reddit, and Wikipedia APIs, respectively. The webpage was designed using HTML/CSS, and put together using the Django framework. This web application is hosted on the Heroku platform.
            <br><br>
![image](https://user-images.githubusercontent.com/6019805/87228784-488d9c80-c358-11ea-8321-6068a492527b.png)
<br/>Api_and_cleaner class and children are in z_scraper.py.

