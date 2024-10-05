import requests
from bs4 import BeautifulSoup

def website(url):
    print('Fetching website content...')

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        html = response.text
        return html

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return ""

def parse_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body

    if body_content:
        return str(body_content)
    
    return ""

def clean_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_tag in soup(["script", "style"]):
        script_tag.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def split_content(website_content, max_length=6000):
    return [
        website_content[i: i + max_length] for i in range(0, len(website_content), max_length)
    ]
