import requests
import datetime
import logging

logging.basicConfig(
    filename='service_monitor.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

services = [
    "https://formit.fake",
    "https://leadsync.fake",
    "https://mailpipe.fake",
    "https://bitdashboard.fake"
]

def check_services():
    for url in services:
        try:
            response = requests.get(url, timeout=5)
            status_code = response.status_code

            if response.ok:
                logging.info(f"{url} | OK | Status code: {status_code}")
            else:
                logging.warning(f"{url} | Warning | Status code: {status_code}")
                print(f"Send alert to Telegram: {url} returned {status_code}")

        except requests.exceptions.RequestException as e:
            logging.error(f"{url} | ERROR | {e}")
            print(f"Send alert to Telegram: {url} not reachable. Error: {e}")

if __name__ == "__main__":
    check_services()