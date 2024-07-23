import os
import requests
import json
import urllib.request
from bs4 import BeautifulSoup

API_KEY = 'INSERT_API_KEY_HERE'

EVENT_KEY = '2024cur'

FOLDER_PATH = './img'

# Headers for the API request
HEADERS = {
    'X-TBA-Auth-Key': API_KEY
}


def fetch_teams(event_key):
    url = f'https://www.thebluealliance.com/api/v3/event/{event_key}/teams'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return [team['team_number'] for team in response.json()]


print(fetch_teams(EVENT_KEY))


def fetch_robot_image(team_key):
    url = f'https://www.thebluealliance.com/api/v3/team/{team_key}/media/2023'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    media = response.json()
    for item in media:
        if item['type'] == 'imgur':
            return f'https://i.imgur.com/{item["foreign_key"]}.jpg'
    return None


def download_image(url, file_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def main():
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    teams = fetch_teams(EVENT_KEY)

    exit(1)
    for team in teams:
        team_key = team['key']
        image_url = fetch_robot_image(team_key)
        if image_url:
            file_name = f"{team_key}.jpg"
            file_path = os.path.join(FOLDER_PATH, file_name)
            download_image(image_url, file_path)
            print(f"Downloaded image for {team_key} to {file_path}")
        else:
            print(f"No image found for {team_key}")


def scrape_robot_image(team_number):
    url = f"https://www.thebluealliance.com/team/{team_number}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to retrieve page for team {team_number}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the image by its class name or id. This may change, so inspect the page to find the correct identifier.
    image_tag = soup.find('a', {'class': 'gallery'})
    image_url = image_tag['href']

    print(image_tag, image_url, sep="\n")

    # Download the image
    image_response = requests.get(image_url)
    print(image_response.status_code)

    if image_response.status_code == 200:
        image_name = f"team_{team_number}_robot_image.jpg"
        with open(image_name, 'wb') as file:
            file.write(image_response.content)
        print(f"Image successfully saved as {image_name}")
    else:
        print(f"Failed to download image for team {team_number}")


if __name__ == '__main__':
    scrape_robot_image(6328)
    main()
