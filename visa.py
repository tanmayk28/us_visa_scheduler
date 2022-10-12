#!/usr/bin/env python

import time
import random
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from consts import base_headers, MY_SCHEDULE_DATE, COUNTRY_CODE, USERNAME, PASSWORD, DATE_URL, TIME_URL, SCHEDULE_ID, APPOINTMENT_URL, FACILITY_ID, COOLDOWN_TIME
from notification import send_notification, push_notification
from errors import LoginError, AccountBannedError, RescheduleError, SessionExpiredError


def get_retry_time():
    return random.randint(40, 50)


class VisaScheduler(object):
    def __init__(self, base_headers):
        self.session = requests.Session()
        self.current_date = MY_SCHEDULE_DATE

        self.session.headers.update(base_headers)

    def login(self):
        login_url = f'https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/users/sign_in'
        r = self.session.get(login_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        data = {
            'utf8': soup.find('input', {'name': 'utf8'})['value'],
            'authenticity_token': soup.find('input', {'name': 'authenticity_token'})['value'],
            'user[email]': USERNAME,
            'user[password]': PASSWORD,
            'policy_confirmed': 1,
            'commit': 'Sign In',
        }
        headers = {
            'Referer': login_url,
        }
        r = self.session.post(login_url, headers=headers, data=data)
        if(r.text.find(USERNAME) != -1):
            print('Login successfully.')
        else:
            raise LoginError(f'Login failed! Will try again.')
    
    def login_with_retries(self):
        for i in range(0, 5):
            try:
                return self.login()
            except LoginError:
                time.sleep(120)
        raise Exception('Login failed too many times.')
        
    def get_date(self):
        r = self.session.get(DATE_URL)
        # check if logged in
        if(r.text.find('error') != -1):
            raise SessionExpiredError('Session expired. Needs to login again.')
        if(len(r.json()) == 0):
            raise AccountBannedError(f'Account is banned, needs to wait for several hours.')
        return r.json()[0]['date']

    def get_time(self, date):
        time_url = TIME_URL % date
        r = self.session.get(time_url)
        if(len(r.json()['available_times']) == 0):
            raise RescheduleError(f'{date} is fully booked.')
        return r.json()['available_times'][-1]
    
    def get_authenticity_token(self):
        headers = {
            'Referer': f'https://ais.usvisa-info.com/en-ca/niv/schedule/{SCHEDULE_ID}/continue_actions',
        }
        r = self.session.get(APPOINTMENT_URL, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        utf8 = soup.find('input', {'name': 'utf8'})['value']
        token = soup.find('input', {'name': 'authenticity_token'})['value']
        return utf8, token

    def is_earlier(self, date):
        my_date = datetime.strptime(self.current_date, "%Y-%m-%d")
        new_date = datetime.strptime(date, "%Y-%m-%d")
        result = my_date > new_date
        print(f'Is {my_date} > {new_date}:\t{result}')
        return result

    def reschedule(self, date):
        time = self.get_time(date)
        utf8, token = self.get_authenticity_token()
        data = {
            "utf8": utf8,
            "authenticity_token": token,
            "confirmed_limit_message": 1,
            "use_consulate_appointment_capacity": "true",
            "appointments[consulate_appointment][facility_id]": FACILITY_ID,
            "appointments[consulate_appointment][date]": date,
            "appointments[consulate_appointment][time]": time,
        }
        headers = {
            'Referer': APPOINTMENT_URL,
        }
        
        r = self.session.post(APPOINTMENT_URL, headers=headers, data=data)
        if(r.text.find('successfully scheduled') != -1):
            self.current_date = date
            print(f'Rescheduled Successfully! {date} {time}')
        else:
            print(f'Reschedule Failed. {date} {time}')


def main():
    scheduler = VisaScheduler(base_headers)
    scheduler.login_with_retries()
    retry_count = 0
    while 1:
        if retry_count > 100:
            break
        try:
            print("------------------")
            print(datetime.today())
            print(f"Retry count: {retry_count}")
            print()

            date = scheduler.get_date()
            print(f"New date: {date}")
            print()
            if scheduler.is_earlier(date):
                scheduler.reschedule(date)
            time.sleep(get_retry_time())

        except SessionExpiredError as e:
            print(e)
            scheduler.login_with_retries()
        except AccountBannedError as e:
            print(e)
            time.sleep(COOLDOWN_TIME)
        except RescheduleError as e:
            print(e)
            retry_count += 1
            time.sleep(get_retry_time())
        except Exception as e:
            print(e)
            time.sleep(300)


if __name__ == "__main__":
    main()
