import os
import time
import requests

TBA_API_KEY = r'qtKgj5EgNArGaDykXISRkNepxhMuQbyEcVkwu2kBNUxtbiSBxKzpgStr0gIXasJP'
EVENT_KEY = 'cur2024'

if not (TBA_API_KEY and EVENT_KEY):
    raise PermissionError("Some keys are missing! Go into code and insert your keys.")

FOLDER_PATH = './components/img'

# Headers for the API request
TBA_HEADERS = {
    'X-TBA-Auth-Key': TBA_API_KEY
}


def fetch_teams(event_key) -> list[int]:
    """
    Fetch the list of teams using an event key.

    :param event_key: The key for the event
    :returns: List of teams
    """

    url = f'https://www.thebluealliance.com/api/v3/event/{event_key}/teams'
    response = requests.get(url, headers=TBA_HEADERS)
    response.raise_for_status()
    return sorted([team['team_number'] for team in response.json()])


def scrape_robot_image(team_number: int):
    """
    Returns the url of the location of the robot image used on TBA.
    This function fails (raises TypeError or returns None) when there is no robot image found on TBA.

    :param team_number: The team number for the robot you're looking for
    :returns: The url of the image
    """

    url = f"https://www.thebluealliance.com/team/{team_number}"



def download_image(team_number: int, image_url: str) -> None:
    """
    Downloads the image from the given url to the appropirate place in code.
    Will download to scoutingapp/src/components/img and will download as team_number.jpeg.

    :param team_number: The team number for the robot
    :param image_url: The url location of the image that needs to be downloaded
    :returns: None
    """




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
        time.sleep(0.5)

        try:
            url = scrape_robot_image(team)
            print(f"{team}: scrape_robot_image ran successfully.")

            if not url:
                print(f"{team}: Failed to retrieve image link.")
                failed_teams[team] = "Failed to retrieve image link."
                continue
            if "imgur" not in url:
                print(f"{team}: Image is not imgur.")
                failed_teams[team] = "Image is not imgur."
                continue

            download_image(team, url)
            print(f'{team}: Success.')
        except TypeError:
            print(f"{team}: Image not found.")
            failed_teams[team] = "Image not found."
        except Exception as e:
            print(f"{team}: {e}")
            failed_teams[team] = e

    if not failed_teams:
        return

    print("NOTE: Some teams did not run properly.")
    print(*failed_teams.items(), sep="\n")

    with open("image_errors.txt", 'w') as err_file:
        for fail in failed_teams.items():
            err_file.write(str(fail) + "\n")


if __name__ == '__main__':
    url = f'https://www.thebluealliance.com/api/v3/team/frc4099/media/2024'
    response = requests.get(url, headers=TBA_HEADERS)
    response.raise_for_status()
    print(response.json())

