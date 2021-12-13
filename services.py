import requests


def linkValidation(url):
    if len(url) < 31:
        return False
    else:
        correctUrl = "https://leetcode.com/problems/"
        if url[0:30] == correctUrl:
            response = requests.get(url)
            if response.status_code == 200:
                return True
            else:
                return False
        else:
            return False


