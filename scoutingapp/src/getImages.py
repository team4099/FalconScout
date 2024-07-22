import os

API_KEY = 'api_key'

EVENT_KEY = 'event_key'

FOLDER_PATH = 'path'

# Headers for the API request
HEADERS = {
    'Auth-Key': API_KEY
}

def fetch_teams(event_key):
    url = f'https://www.thebluealliance.com/api/v3/event/{event_key}/teams'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

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

if __name__ == '__main__':
    main()
