- [Introduction](#org1feee9f)
  - [How it works](#org0c0609d)
- [User Interface](#org8a8f54f)
- [Prepare the environment](#orgd750144)
- [Access to the service](#orgeabc49f)
  - [Access through User Interface](#org282d74b)
  - [Access through API](#orgc6bb1d3)
    - [Analyze the sentiment of one or more topics](#org6aa98cb)
    - [Ignore neutral values](#org598b43e)
    - [Analyze recent Tweets (last hour)](#org8981d64)
    - [Combine keywords](#org3ff6573)
    - [Use Twitter operators](#orgfee348d)



<a id="org1feee9f"></a>

# Introduction

JA-Sentiment-Analyzer (JASA), is a *Just Another* project which aims to provide a simple service to quickly know the sentiment of a particular topic or several topics related to each other.


<a id="org0c0609d"></a>

## How it works

JASA is a server that provides REST APIs for its integration written through the Python language. More precisely, with the help of the [FastAPI](https://fastapi.tiangolo.com/) framework, JASA allows queries to be made through the API provided by [Twitter](https://twitter.com/).

Once the Tweets related to the query made are obtained, JASA will express a sentiment value as an output of the process. The sentiment value is generated by summing the sentiment of all Tweets related to the same topic in a proportional way to the number of retweets, replies, mentions and likes. Finally, the sentiment value for each individual Tweet is assigned thanks to the [cardiffnlp/tweeteval](https://github.com/cardiffnlp/tweeteval/blob/main/README.md) model also available through [Huggingface](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment).


<a id="org8a8f54f"></a>

# User Interface

JA-Sentiment-Analyzer is present with a `User Interface` that allows you to easily perform queries quickly across the API layer.


<a id="orgd750144"></a>

# Prepare the environment

First, download the repository.

```sh
git clone https://github.com/ZappaBoy/JA-Sentiment-Analyzer
```

Next, access the folder and create a `.env` file.

```sh
cd JA-Sentiment-Analyzer
touch .env
```

Edit the `.env` file by inserting the necessary environment variables. You must have Twitter access codes, to obtain these codes consult the [Twitter developer documentation](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api). An example of environment variables is as follows:

```sh
ENVIRONMENT=production # System environment stage
PORT=3000 # Port on which the service will be active
USE_USER_CONTEXT=False # Enable or disable the use of the Twitter user context
USE_APP_CONTEXT=True # Enable or disable the use of the Twitter application context
LABEL_30_DAY=YOUR_LABEL_30_DAY # The 30 Day Twitter label needed to access recent tweets
LABEL_FULL_ARCHIVE=YOUR_LABEL_FULL_ARCHIVE # The Full Archive Twitter label needed to access popular tweets
CONSUMER_KEY=YOUR_CONSUMER_KEY # Twitter Consumer Key
CONSUMER_KEY_SECRET=YOUR_CONSUMER_KEY_SECRET # Twitter Consumer Key Secret
BEARER_TOKEN=YOUR_BEARER_TOKEN # Twitter Bearer Token
ACCESS_TOKEN=YOUR_ACCESS_TOKEN # Twitter Access Token
ACCESS_TOKEN_SECRET=YOUR_ACCESS_TOKEN_SECRET # Twitter Access Token Secret
LOG_LEVEL=debug # Fastapi/starlette log level
ALLOWED_HOSTS=localhost,your.own.domain,your.other.domain # Allowed hosts, you can also set 0.0.0.0 to enable all hosts
```

Finally, start the whole JA-Sentiment-Analyzer system with the `docker-compose` utility.

```sh
docker-compose up --build -d # or "docker compose up --build -d" for newer docker version
```

Note that the startup process may take a few minutes depending on your connection speed


<a id="orgeabc49f"></a>

# Access to the service


<a id="org282d74b"></a>

## Access through User Interface

Once initialization is complete, you can access the `User Interface` at `http://{{YOUR_DOMAIN}}:{{YOUR_PORT}}/engine`.


<a id="orgc6bb1d3"></a>

## Access through API

Finally, JASA provides the \`/api/analyze-keywords\` endpoint to allow the integration of the system with others. The call is of type \`GET\` and it is possible to define the behaviour of the system through parameters:

-   \`keywords\` (Required) (String Array) - Defines an array of keywords divided by a comma;
-   \`ignore\_neutral\` (Boolean) - If set to \`True\` allows to force sentiment to only \`POSITIVE\` and \`NEGATIVE\` values ignoring neutral values;
-   \`timeframe\` (String) - If set it will search for recent Tweets. Possible values are of the type \`1m\` \`4h\` \`12d\` \`3w\` \`1M\` and cannot exceed 30 days.
-   \`combine\` (Boolean) - If set to \`True\` allows you to combine all \`keywords\` into a single query. This allows for Twitter-supported query operators, see the official Twitter [documentation](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query) for more information.


<a id="org6aa98cb"></a>

### Analyze the sentiment of one or more topics

```sh
curl -X GET 'YOUR_DOMAIN:YOUR_PORT/api/analyze-keywords?keywords=Bitcoin,Covid,Cryptocurrencies'

{
   "result":{
      "Bitcoin": "POSITIVE",
      "Covid": "NEGATIVE",
      "Cryptocurrencies": "NEUTRAL"
   }
}
```


<a id="org598b43e"></a>

### Ignore neutral values

```sh
curl -X GET 'YOUR_DOMAIN:YOUR_PORT/api/analyze-keywords?keywords=Bitcoin,Covid,Cryptocurrencies&ignore_neutral=True'

{
   "result":{
      "Bitcoin":"POSITIVE",
      "Covid":"NEGATIVE",
      "Cryptocurrencies":"POSITIVE" # Positive due to the greater optimism compared to pessimism
   }
}
```


<a id="org8981d64"></a>

### Analyze recent Tweets (last hour)

```sh
curl -X GET 'YOUR_DOMAIN:YOUR_PORT/api/analyze-keywords?keywords=Bitcoin,Covid,Cryptocurrencies&timeframe=1h'

{
   "result":{
      "Bitcoin": "NEGATIVE",
      "Covid": "NEGATIVE",
      "Cryptocurrencies": "NEGATIVE"
   }
}
```


<a id="org3ff6573"></a>

### Combine keywords

```sh
curl -X GET 'YOUR_DOMAIN:YOUR_PORT/api/analyze-keywords?keywords=Bitcoin,Cryptocurrencies&combine=True'

{
   "result":{
      "Bitcoin Cryptocurrencies": "NEUTRAL" # Analyze Tweets with both 'Bitcoin' and 'Cryptocurrencies' keywords
   }
}
```


<a id="orgfee348d"></a>

### Use Twitter operators

```sh
curl -X GET 'YOUR_DOMAIN:YOUR_PORT/api/analyze-keywords?keywords=Bitcoin,@elonmusk&combine=True'

{
   "result":{
      "Bitcoin @elonmusk": "NEUTRAL" # Analyze Tweets with 'Bitcoin' keyword related to '@elonmusk' user
   }
}
```

```sh
curl -X GET 'YOUR_DOMAIN:YOUR_PORT/api/analyze-keywords?keywords=Bitcoin,place:new%20york%20city&combine=True'

{
   "result": {
      "Bitcoin place: new york city": "POSITIVE" # Analyze Tweets with 'Bitcoin' keyword from New York City
   }
}
```
