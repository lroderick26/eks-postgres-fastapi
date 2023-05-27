import os
from urllib.parse import quote
from transformers import pipeline
import boto3
from bs4 import BeautifulSoup
import requests
import io
import re
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

BASE_URL = 'http://www.imsdb.com'
SCRIPTS_DIR = ''
SCRIPTS_BUCKET = 'lwtdemo' # created by our terraform script
POSTGRES_URI = os.getenv("POSTGRES_URI") # already running in cluster

# Create a boto3 session for accessing AWS resources
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
s3 = session.resource("s3")

# Connect and instantialize database
engine = create_engine(os.getenv("POSTGRES_URI"))

conn = engine.connect()
conn.autocommit = True

files = ['create_schema.sql', 'create_table.sql']

for file in files:
    with open(f"./sql/{file}") as asql:
        query = text(asql.read())
        # query = asql.read()
        print(query)
        conn.execute(query)
        conn.commit()



classifier = pipeline("text-classification", model='bhadresh-savani/distilbert-base-uncased-emotion',
                          top_k=None)

def clean_script(input_text):
    input_text = input_text.replace('Back to IMSDb', '')
    input_text = input_text.replace('''<b><!--
</b>if (window!= top)
top.location.href=location.href
<b>// -->
</b>
''', '')
    input_text = input_text.replace('''          Scanned by http://freemoviescripts.com
          Formatting by http://simplyscripts.home.att.net
''', '')
    return input_text.replace(r'\r', '')


def get_script(relative_link):
    tail = relative_link.split('/')[-1]
    print('fetching %s' % tail)
    script_front_url = BASE_URL + quote(relative_link)
    print(script_front_url)
    front_page_response = requests.get(script_front_url)
    front_soup = BeautifulSoup(front_page_response.text, "html.parser")
    try:
        script_link = front_soup.find_all('p', align="center")[0].a['href']
    except IndexError:
        print('%s has no script :(' % tail)
        return None, None
    if script_link.endswith('.html') and '/scripts/' in script_link:
        title = script_link.split('/')[-1].split(' Script')[0]
        script_url = BASE_URL + script_link
        print(script_url)
        script_soup = BeautifulSoup(requests.get(script_url).text, "html.parser")
        script_text = script_soup.find_all('td', {'class': "scrtext"})[0].get_text()
        script_text = clean_script(script_text)
        # try to get the year too
        btags = front_soup.findAll("b")
        date_info = None
        for tag in btags:
            if tag.text == "Script Date":
                date_info = tag.next_sibling
        return title, script_text, date_info
    else:
        print('%s is a pdf :(' % tail)
        return None, None, None

def run_sentiment_analysis(data):
    # sentiment_pipeline = pipeline("sentiment-analysis")
    evaluation = classifier(data, )
    return evaluation


def upload_to_s3(script_data, script_path):
    buff = io.BytesIO()
    buff.write(script_data)
    s3.Object(SCRIPTS_BUCKET, 'scripts/' + script_path).put(Body=buff.getvalue())
    return True


def find_all_lesbians(input_text):
    pattern = r'\b[^.]*{}[^.]*\b'.format("lesbian")
    all_instances = re.findall(pattern, input_text)
    return all_instances


if __name__ == "__main__":
    response = requests.get('http://www.imsdb.com/all-scripts.html')
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all('p')
    print(len(paragraphs))
    # print(paragraphs)
    for p in paragraphs[1:]:
        relative_link = p.a['href']
        title, script, date_info = get_script(relative_link)
        if not script:
            pass
        else:
            script_name = SCRIPTS_DIR + title.strip('.html') + '.txt'
            # Upload to s3 just because we want a backup
            upload_to_s3(script.encode('ascii','ignore'), script_name)
            # find all instances of the word "lesbian" in a sentence and return the sentence for sentiment analysis
            sentences = find_all_lesbians(script)
            sentiments = []
            for sentence in sentences:
                sentiment = run_sentiment_analysis(sentence)
                sentiments.append((sentence, sentiment))
            # insert into the database
            for sentence, sentiment in sentiments:
                sadness_score = float([s['score'] for s in sentiment if s['label'] == 'sadness'][0])
                joy_score = float([s['score'] for s in sentiment if s['label'] == 'joy'][0])
                love_score = float([s['score'] for s in sentiment if s['label'] == 'love'][0])
                anger_score =float([s['score'] for s in sentiment if s['label'] == 'anger'][0])
                fear_score = float([s['score'] for s in sentiment if s['label'] == 'fear'][0])
                surprise_score = float([s['score'] for s in sentiment if s['label'] == 'surprise'][0])
                insert_statement = "INSERT INTO script_records (title, date_info, sentence, sentiment, sadness, joy, love, anger, fear, suprise) VALUES (:title, :date_info, :sentence, :sentiment, :sadness, :joy, :love, :anger, :fear, :suprise) "
                print(insert_statement)
                params = {'title': title,
                        'date_info': date_info,
                        'sentence': sentence,
                        'sentiment': sentiment,
                        'sadness': sadness_score,
                        'joy': joy_score,
                        'love': love_score,
                        'anger': anger_score,
                        'fear': fear_score,
                        'surprise': surprise_score}
                conn.execute(insert_statement, **params)


