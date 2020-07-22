# Jetmap

## Purpose

Jetmap is designed to allow scraping of Twitter searches and/or accounts for printing to screen and saving to CSV file. The name comes [here](https://divergentdave.github.io/nsa-o-matic/).  

## Requirements

 - A Twitter Developer Account and associated access token, access secret, API key and API secret;  
 - `tweepy`; and  
 - Python 3.6 or above (needs to support f-strings).  
 - config.ini file in the following format

```ini
[DATA]
access_token = <insert>
access_secret = <insert>
api_key = <insert>
api_secret = <insert>
```

## Status

Under development, there are still some improvments and code refactoring etc. etc.   

## TO DO

- general error checking (e.g. check if CSV exists before writing header row)
- add output to Slack channel
- extract defanged URLs and convert for #opendir matches
- integrate parsing of captured data with Virus Total API.