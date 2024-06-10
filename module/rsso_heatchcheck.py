import requests


def verify_login(rsso_url, username, password):
    login_url = f"{rsso_url}/arsys/shared/login.jsp"

    # Create a session to maintain cookies
    session = requests.Session()

    # Perform login request
    try:
        response = session.post(login_url, data={"username": username, "password": password})
        if response.status_code == 200:
            # Check if login was successful
            if "logout" in response.url:
                print("Login successful")
            else:
                print("Login failed: Invalid credentials")
        else:
            print(f"Login failed. Status code: {response.status_code}")
    except Exception as e:
        print(f"Login failed. Error: {str(e)}")


if __name__ == "__main__":
    # Replace these values with your BMC RSSO URL, username, and password
    rsso_url = "http://your_bmcrsso_url"
    username = "your_username"
    password = "your_password"

    verify_login(rsso_url, username, password)

== == == =
import requests
import time


def check_health(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Health check passed for {url}")
        else:
            print(f"Health check failed for {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Health check failed for {url}. Error: {str(e)}")


if __name__ == "__main__":
    # Replace this URL with your BMC RSSO application URL
    rsso_url = "http://your_bmcrsso_application_url"

    while True:
        check_health(rsso_url)
        time.sleep(60)  # Check every 60 seconds
== ==

import requests
import time


def check_health(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Health check passed for {url}")
        else:
            print(f"Health check failed for {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Health check failed for {url}. Error: {str(e)}")


if __name__ == "__main__":
    # Replace these URLs with your TSCO console and dashboard URLs
    console_url = "http://your_tcs_console_url"
    dashboard_url = "http://your_tcs_dashboard_url"

    while True:
        check_health(console_url)
        check_health(dashboard_url)
        time.sleep(60)  # Check every 60 seconds
== == =


import requests
import time


def authenticate_rsso(rsso_url, username, password):
    login_url = f"{rsso_url}/arsys/shared/login.jsp"

    session = requests.Session()

    try:
        response = session.post(login_url, data={"username": username, "password": password})
        if response.status_code == 200 and "logout" in response.url:
            print("RSSO authentication successful")
            return session
        else:
            print("RSSO authentication failed. Please check your credentials.")
            return None
    except Exception as e:
        print(f"RSSO authentication failed. Error: {str(e)}")
        return None


def check_health(session, tsco_url):
    try:
        response = session.get(tsco_url)
        if response.status_code == 200:
            print(f"Health check passed for {tsco_url}")
        else:
            print(f"Health check failed for {tsco_url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Health check failed for {tsco_url}. Error: {str(e)}")


if __name__ == "__main__":
    # Replace these values with your BMC RSSO URL, username, password, and TSCO application URL
    rsso_url = "http://your_bmcrsso_url"
    username = "your_username"
    password = "your_password"
    tsco_url = "http://your_tsco_application_url"

    session = authenticate_rsso(rsso_url, username, password)
    if session:
        while True:
            check_health(session, tsco_url)
            time.sleep(60)  # Check every 60 seconds
    else:
        print("RSSO authentication failed. Exiting...")

