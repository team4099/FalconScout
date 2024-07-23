import os
import requests
import json
from urllib.request import Request, urlopen
import time
from bs4 import BeautifulSoup

TBA_API_KEY = 'INSERT_HERE'
IMGUR_CLIENT_ID = 'INSERT_HERE'
IMGUR_ETAG = 'INSERT_HERE'

EVENT_KEY = '2024cur'

FOLDER_PATH = './components/img'

# Headers for the API request
TBA_HEADERS = {
    'X-TBA-Auth-Key': TBA_API_KEY
}

IMGUR_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Referer': 'https://imgur.com/',
    'Authorization': f"Client-ID {IMGUR_CLIENT_ID}",
    "ETag": IMGUR_ETAG,
}


def fetch_teams(event_key):
    url = f'https://www.thebluealliance.com/api/v3/event/{event_key}/teams'
    response = requests.get(url, headers=TBA_HEADERS)
    response.raise_for_status()
    return [team['team_number'] for team in response.json()]


def fetch_robot_image(team_key):
    url = f'https://www.thebluealliance.com/api/v3/team/{team_key}/media/2023'
    response = requests.get(url, headers=TBA_HEADERS)
    response.raise_for_status()
    media = response.json()
    for item in media:
        if item['type'] == 'imgur':
            return f'https://i.imgur.com/{item["foreign_key"]}.jpg'
    return None


def main():
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    teams = fetch_teams(EVENT_KEY)

    for team in teams:
        time.sleep(1)
        scrape_robot_image(team)


def scrape_robot_image(team_number: int) -> None:
    url = f"https://www.thebluealliance.com/team/{team_number}"
    response = requests.get(url, headers=TBA_HEADERS)

    if response.status_code != 200:
        print(f"{response.status_code}: Failed to retrieve page for team {team_number}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the image by its class name or id. This may change, so inspect the page to find the correct identifier.
    image_tag = soup.find('a', {'class': 'gallery'})
    image_url = image_tag['href']

    if not image_url:
        print(f"No image found for team {team_number}")
        return

    print(image_tag, image_url, sep="\n")
    image_ending = image_url[-3:]
    image_hash = image_url.split("/")[3].removesuffix(".jpg").removesuffix(".png")
    image_url = f"https://api.imgur.com/3/image/{image_hash}"
    print(image_url)

    # Download the image
    image_response = requests.get(image_url, headers=IMGUR_HEADERS, stream=True)
    print("*", image_response)
    print("***", image_response.headers)
    image_response.raise_for_status()

    file_path = os.path.join(FOLDER_PATH, f"{team_number}.{image_ending}")
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

    print(f"Downloaded image for {team_number} to {file_path}")


if __name__ == '__main__':
    print(fetch_teams(EVENT_KEY))
    scrape_robot_image(6328)
    #main()
