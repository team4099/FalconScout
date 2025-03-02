import os
import time
import requests

TBA_API_KEY = r'zFwttaDMMWBKxjXaPSsMJK14pMvwYfgulFeeMermxHqnjuBMQll6hkV7mBl39jDa'
IMGUR_CLIENT_ID = r'e6b25fcb319d82d'
IMGUR_ETAG = r'W/"12715af20eb36231834f51357e0d0690f2e54a7e"'
EVENT_KEY = r'2025vapor'

if not (TBA_API_KEY and IMGUR_CLIENT_ID and IMGUR_ETAG and EVENT_KEY):
    raise PermissionError("Some keys are missing! Go into code and insert your keys.")

FOLDER_PATH = 'public'

# Headers for the API request
TBA_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Referer': 'https://www.thebluealliance.com/',
    'X-TBA-Auth-Key': TBA_API_KEY
}

IMGUR_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Referer': 'https://imgur.com/',
    'Authorization': f"Client-ID {IMGUR_CLIENT_ID}",
    "ETag": IMGUR_ETAG,
}


def fetch_teams(event_key: str) -> list[int]:
    """
    Fetch the list of teams using an event key.

    :param event_key: The key for the event
    :returns: List of teams
    """

    url = f'https://www.thebluealliance.com/api/v3/event/{event_key}/teams'
    response = requests.get(url, headers=TBA_HEADERS)
    response.raise_for_status()
    return sorted([team['team_number'] for team in response.json()])


def scrape_robot_url(team_number: int) -> str:
    """
    Returns the url of the location of the robot image used on TBA.
    This function fails (raises TypeError or returns None) when there is no robot image found on TBA.

    :param team_number: The team number for the robot you're looking for
    :returns: The url of the image
    """

    url = f'https://www.thebluealliance.com/api/v3/team/frc{team_number}/media/{EVENT_KEY[:4]}'
    response = requests.get(url, headers=TBA_HEADERS)
    response.raise_for_status()
    data = [x for x in response.json() if x['type'] not in ['avatar', 'youtube']]
    return data[0]['direct_url']


def download_image(team_number: int, image_url: str, image_host: str) -> None:
    """
    Downloads the image from the given url to the appropirate place in code.
    Will download to scoutingapp/src/components/img and will download as team_number.jpeg.

    :param team_number: The team number for the robot
    :param image_url: The url location of the image that needs to be downloaded
    :param image_host: Website hosting image (instagram | imgur)
    :returns: None
    """

    if image_host == "imgur":
        image_hash = image_url.split("/")[3].removesuffix(".jpg").removesuffix(".jpeg").removesuffix(".png")
        image_ending = image_url.split(".")[-1]
        image_ending = "jpeg" if image_ending == "jpg" else image_ending

        image_url = f'https://i.imgur.com/{image_hash}.{image_ending}'

        image_response = requests.get(image_url, headers=IMGUR_HEADERS)
    elif image_host == "instagram":
        image_url = f'https://thebluealliance.com/{image_url}'
        image_ending = "jpeg"

        image_response = requests.get(image_url, headers=TBA_HEADERS)
    else:
        return

    image_response.raise_for_status()

    file_path = os.path.join(FOLDER_PATH, f"{team_number}.{image_ending}")

    with open(file_path, 'wb') as f:
        f.write(image_response.content)

    return


def main(teams: tuple[int] = ()) -> None:
    """
    Main function.

    :param teams: List of teams, optional, should only be inputted as argument when debugging code
    :returns: None
    """

    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    if not teams:
        teams = fetch_teams(EVENT_KEY)

    failed_teams = {}
    for team in teams:
        print(f'{team}: Starting...')
        time.sleep(2)  # anti 429

        try:
            url = scrape_robot_url(team)

            if not url:
                print(f"{team}: Failed to retrieve image link.")
                failed_teams[team] = "Failed to retrieve image link."
                continue
            if "imgur" in url:
                download_image(team, url, "imgur")
            elif "instagram" in url:
                download_image(team, url, "instagram")
            else:
                print(f"{team}: Image host not recognized.")
                failed_teams[team] = "Image host not recognized."

            print(f'{team}: Success.')
        except (TypeError, IndexError):
            print(f"{team}: Image not found.")
            failed_teams[team] = "Image not found."
        except Exception as e:
            print(f"{team}: {e}")
            failed_teams[team] = e

    if not failed_teams:
        return

    print("NOTE: Some teams did not run properly.")
    print(*failed_teams.items(), sep="\n")

    with open("./image_errors.txt", 'w') as err_file:
        for fail in failed_teams.items():
            err_file.write(str(fail) + "\n")


if __name__ == '__main__':
    main()
