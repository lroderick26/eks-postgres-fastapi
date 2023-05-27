# Data Pipeline

This is the image for running the data pipeline that scrapes the data via BeautifulSoup and inserts it into our database.


## Sentiment Pipeline Info

For more information on the package:
https://pypi.org/project/transformers/
https://huggingface.co/blog/sentiment-analysis-python

From this pipeline, we use the Distilbert base uncased emotion sentiment: 
"Distilbert-base-uncased-emotion is a fine-tuned model for detecting emotions in texts, including sadness, joy, love, 
anger, fear and surprise."



## Test & Run Locally
See /api/README.md for more info. You'll need to run that docker-compose file first to make sure the database and api are 
also running. 

After getting the api version of the docker-compose file up, you can use: 

`docker-compose up -d --build` 

in the current directory

