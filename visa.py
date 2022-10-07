# -*- coding: utf8 -*-

import time
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from notification import send_notification, push_notification


# def MY_CONDITION(month, day): return int(month) == 11 and int(day) >= 5
def MY_CONDITION(month, day): 
    return True # No custom condition wanted for the new scheduled date


def get_date():
    global last_yatry_cookie

    if last_yatry_cookie == "":
        driver.get(DATE_URL)
        if not is_logged_in():
            login()
            return get_date()
        else:
            content = driver.find_element(By.TAG_NAME, 'pre').text
            date = json.loads(content)
            last_yatry_cookie = "_yatri_session=" + driver.get_cookie("_yatri_session")["value"]
            return date
    else:
        headers = base_headers
        headers["Cookie"] = last_yatry_cookie
        r = requests.get(DATE_URL, headers=headers)
        print(r.text)
        last_yatry_cookie = r.headers['Set-Cookie'].split(";")[0]
        print(last_yatry_cookie)
        return r.json()


def get_time(date):
    global last_yatry_cookie

    print(f" Retrieving latest date for {date}")
    time_url = TIME_URL % date
    headers = base_headers
    headers["Cookie"] = last_yatry_cookie
    r = requests.get(time_url, headers=headers)
    data = json.loads(r.text)
    time = data.get("available_times")[-1]
    print(f"latest available time for {date}: {time}")
    last_yatry_cookie = r.headers['Set-Cookie'].split(";")[0]
    print(last_yatry_cookie)
    return time
    # time_url = TIME_URL % date
    # driver.get(time_url)
    # content = driver.find_element(By.TAG_NAME, 'pre').text
    # data = json.loads(content)
    # time = data.get("available_times")[-1]
    # print(f"Got time successfully! {date} {time}")
    # return time

def get_authenticity_token():
    global last_yatry_cookie

    headers = base_headers
    headers["Referer"] = "https://ais.usvisa-info.com/en-ca/niv/schedule/42238236/continue_actions"
    headers["Cookie"] = last_yatry_cookie
    r = requests.get(APPOINTMENT_URL, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    utf8 = soup.find('input', {'name': 'utf8'})['value']
    token = soup.find('input', {'name': 'authenticity_token'})['value']
    print(token)
    last_yatry_cookie = r.headers['Set-Cookie'].split(";")[0]
    print(last_yatry_cookie)
    return utf8, token


def reschedule(date):
    global last_yatry_cookie, EXIT
    print(f"Starting Reschedule ({date})")

    time = get_time(date)
    # time = "09:00"
    utf8, token = get_authenticity_token()

    data = {
        "utf8": utf8,
        "authenticity_token": token,
        "confirmed_limit_message": 1,
        "use_consulate_appointment_capacity": "true",
        "appointments[consulate_appointment][facility_id]": FACILITY_ID,
        "appointments[consulate_appointment][date]": date,
        "appointments[consulate_appointment][time]": time,
    }

    headers = base_headers
    headers["Referer"] = APPOINTMENT_URL
    headers["Cookie"] = last_yatry_cookie
    # headers = {
    #     "User-Agent": driver.execute_script("return navigator.userAgent;"),
    #     "Referer": APPOINTMENT_URL,
    #     "Cookie": "_yatri_session=" + driver.get_cookie("_yatri_session")["value"]
    # }

    r = requests.post(APPOINTMENT_URL, headers=headers, data=data)
    last_yatry_cookie = r.headers['Set-Cookie'].split(";")[0]
    print(last_yatry_cookie)
    if(r.text.find('successfully scheduled') != -1):
        msg = f"Rescheduled Successfully! {date} {time}"
        send_notification(msg)
        MY_SCHEDULE_DATE = date
        print("updated schedule date to %s", date)
        # EXIT = True
    else:
        print(r.text)
        msg = f"Reschedule Failed. {date} {time}"
        send_notification(msg)


def is_logged_in():
    content = driver.page_source
    if(content.find("error") != -1):
        return False
    return True


def print_dates(dates):
    print("Available dates:")
    for d in dates:
        print("%s \t business_day: %s" % (d.get('date'), d.get('business_day')))
    print()


last_seen = None


def get_available_date(dates):
    global last_seen

    def is_earlier(date):
        my_date = datetime.strptime(MY_SCHEDULE_DATE, "%Y-%m-%d")
        new_date = datetime.strptime(date, "%Y-%m-%d")
        result = my_date > new_date
        print(f'Is {my_date} > {new_date}:\t{result}')
        return result

    print("Checking for an earlier date:")
    for d in dates:
        date = d.get('date')
        if is_earlier(date):
            return date
        # if is_earlier(date) and date != last_seen:
        #     _, month, day = date.split('-')
            # if(MY_CONDITION(month, day)):
            #     last_seen = date
            #     return date


if __name__ == "__main__":
    # login()
    retry_count = 0
    while 1:
        if retry_count > 100:
            break
        try:
            print("------------------")
            print(datetime.today())
            print(f"Retry count: {retry_count}")
            print()

            dates = get_date()[:5]
            if not dates:
              msg = "List is empty"
              send_notification(msg)
              EXIT = False
            print_dates(dates)
            date = get_available_date(dates)
            print()
            print(f"New date: {date}")
            if date:
                reschedule(date)
                push_notification(dates)

            if(EXIT):
                print("------------------exit")
                break

            if not dates:
              msg = "List is empty"
              send_notification(msg)
              #EXIT = True
              time.sleep(COOLDOWN_TIME)
            else:
              time.sleep(RETRY_TIME)

        except:
            retry_count += 1
            time.sleep(EXCEPTION_TIME)

    if(not EXIT):
        send_notification("HELP! Crashed.")
