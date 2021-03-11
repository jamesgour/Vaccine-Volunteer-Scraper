import requests, os, difflib, smtplib
from bs4 import BeautifulSoup
from pprint import pprint
from time import sleep

# Specify whether this is the first time running the script or not
# Note: this should be switched after the script runs the first time
first_run = False

# Phone number, Gmail, & Gmail app PW
PHONE_NUMBER_EMAIL = os.environ.get('PHONE_NUMBER_EMAIL')
GMAIL = os.environ.get('GMAIL')
GMAIL_APP_PW =  os.environ.get('GMAIL_APP_PW')

# Hands On Phoenix vaccine website URL
url = 'https://www.handsonphoenix.org/vaccinatestate48'

# Define Functions
def main():
    if first_run == True:
        scrape_volunteer_webpage(url, 'Baseline Webpage.html')
        return 'Scraped Baseline Webpage'

    else:
        scrape_volunteer_webpage(url, 'Comparison Webpage.html')
        diff = html_diff('Baseline Webpage.html', 'Comparison Webpage.html')
        if diff == False:
            print('No change to webpage.')
        else:
            send_text_alert()
            print('Changes detected in webpage!')


def scrape_volunteer_webpage(url, html_page_name):
    # Get page & soup
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Parse through results & save page content
    results = soup.find(id='main_content')
    page_content = results.find_all('div', {'class': 'content'})

    # Loop through all page_content elements & write to html file
    with open (html_page_name, 'w') as file:
        for element in page_content:
            file.write(str(element.text))

def html_diff(page_1, page_2):
    file_1 = open(page_1, 'r').readlines()
    file_2 = open(page_2, 'r').readlines()

    # Write differences between webpages to a html file
    htmlDiffer = difflib.HtmlDiff()
    htmldiffs = htmlDiffer.make_file(file_1, file_2)

    with open('Webpage Differences.html', 'w') as outfile:
        outfile.write(htmldiffs)

    # Compare if files are the same
    if os.path.getsize(page_1) == os.path.getsize(page_2):
            if open(page_1,'r').read() == open(page_2,'r').read():
                return False

    else:
        return True

def send_text_alert():
    # Useful overview video https://www.youtube.com/watch?v=JRCJ6RtE3xU
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(GMAIL, GMAIL_APP_PW)

        subject = 'Webpage Change Detected'
        body = 'A change has been detected at https://www.handsonphoenix.org/vaccinatestate48!'
        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(GMAIL, GMAIL, msg)

# Run the scraper
main()
