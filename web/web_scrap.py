import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = 'https://unmethours.com'

def href_store(url=BASE_URL):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', id='question-list')
    anchor_elements = s.find_all('h2')

    hrefs = []
    questions = []
    for element in anchor_elements:
        a_tag = element.find('a')
        if a_tag and a_tag.get('href'):
            hrefs.append(BASE_URL + a_tag.get('href'))
            questions.append(a_tag.text.strip())
    return hrefs, questions

def extract_qna(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    all_editables = soup.find_all('div', class_='js-editable-content')

    # First is the question
    question_text = all_editables[0].get_text(strip=True) if all_editables else ''

    # Rest are answers
    answer_texts = [div.get_text(strip=True) for div in all_editables[1:]] if len(all_editables) > 1 else []

    return question_text, "\n---\n".join(answer_texts)

# Main
question_urls, question_titles = href_store()
data = []

for url, title in zip(question_urls[:], question_titles[:]):  # limit for demo
    print(f"Scraping: {title}")
    try:
        question, answer = extract_qna(url)
        data.append({
            'question_url': url,
            'question': question,
            'answer': answer or 'No answer'
        })
        time.sleep(1)
    except Exception as e:
        print(f"Error scraping {url}: {e}")

df = pd.DataFrame(data)
print(df['answer'][9])
