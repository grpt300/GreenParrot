import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
            return True
        else:
            print(f"Health check failed for {tsco_url}. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Health check failed for {tsco_url}. Error: {str(e)}")
        return False


def send_email(sender_email, sender_password, receiver_email, subject, message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email notification sent successfully")
        server.quit()
    except Exception as e:
        print(f"Failed to send email notification. Error: {str(e)}")


if __name__ == "__main__":
    # Replace these values with your BMC RSSO URL, username, password, TSCO application URL, and email settings
    rsso_url = "http://your_bmcrsso_url"
    username = "your_username"
    password = "your_password"
    tsco_url = "http://your_tsco_application_url"

    sender_email = "your_email@gmail.com"
    sender_password = "your_email_password"
    receiver_email = "receiver_email@example.com"

    session = authenticate_rsso(rsso_url, username, password)
    if session:
        while True:
            if not check_health(session, tsco_url):
                send_email(sender_email, sender_password, receiver_email, "TSCO Health Check Failed",
                           f"Health check failed for {tsco_url}. Please investigate.")
            time.sleep(60)  # Check every 60 seconds
    else:
        print("RSSO authentication failed. Exiting...")
