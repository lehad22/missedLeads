import requests
import time
import logging
from datetime import datetime
import schedule

TOKEN = "TOKEN"
CHAT_ID = "CHAT_ID"
services = [
    "https://formit.fake",
    "https://datavalidator.fake",
    "https://leadsync.fake",
    "https://bitdashboard.fake"
]
logging.basicConfig(
    filename='service_monitor.log', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s'
)

error_cnt = {}
for url in services:
    error_cnt[url] = {
        "last_code": None,
        "repeat_count": 0
    }
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        logging.error(f"Ошибка при отправке {e}")
def check_services():
    for url in services:
        try:
            start = time.time()
            response = requests.post(url, timeout=10)
            end = time.time()
            response_time = end - start
            status_code = response.status_code

            log_entry = f"{url} | Код: {status_code} | Время отклика: {response_time} сек"
            logging.info(log_entry)

            notCorrect = False
            if not (200 <= response.status_code < 300):
                notCorrect = True
            if response_time > 2:
                notCorrect = True

            last = error_cnt[url]["last_code"]
            if status_code == last:
                error_cnt[url]["repeat_count"] += 1
            else:
                error_cnt[url]["last_code"] = status_code
                error_cnt[url]["repeat_count"] = 1

            if error_cnt[url]["repeat_count"] >= 3:
                notCorrect = True

            if notCorrect:
                msg = (
                    f"Проблема с сервисом {url}\n"
                    f"Код: {status_code}, Повторений: {error_cnt[url]['repeat_count']}, "
                    f"Отклик: {response_time} сек, Время: {datetime.now().strftime('%H:%M:%S')}"
                )
                print(msg)
                logging.warning(msg)
                send_telegram_message(msg)
        except requests.exceptions.RequestException as e:
            msg = f"Сервис {url} недоступен. {e}"
            print(msg)
            logging.error(msg)
            send_telegram_message(msg)

schedule.every(5).minutes.do(check_services)
check_services()

while True:
    schedule.run_pending()
    time.sleep(1)