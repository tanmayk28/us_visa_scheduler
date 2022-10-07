import random
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

last_yatry_cookie = "_yatri_session=WUg0QzNERkZ5TTVnOU1pcHV3VjhDRDZDRS9wWjJCejRML2F6T0xMSnc5ZzVEd0tqbXU3TUtwNlpLM3poTk5Lam45b1FBazg2UHdmOFJPR0RUSWExVFpDeDZlZlVqUGxiRTVSS3ZPcXRpdEhpeXZUYVNoamhoaXVYMG92ZU51Z3lvV0d5OEZ0b1ZYc1lyYUozZU5aOFRVb3kvUDRsdmhzdklseTJxa1NQZTJ0Mi9MQWhES08rcDMxUHZsd21jK25tcXliaG9uWmVEeVdEKzUraHVnVGkrUi9FMXR1U280QmJ1b05YQ2ZrMTJWN0ptTGRoSkUxSC9qWW5keWxFZ1V1cHc1RWJmYXVjWE9LdWViWFNMMHk5Rk5TQlZZcEllaVpnZkVIY0dqYXNpRktHdVNCcHUyaS83ZTJPSjZFZGlzZ0pUSTJoZmxUYXMxcDFJcmxpTFFCMmVhNEZobDZkNmJlcFdqUzhmMlFZSzdqT3BITk9oK0hpUXhBcXZDN0hMaHo1eXdXSVhYZWZKUXJmc2JaSXllbTNIbmRuT2UyRUlhZThubCs0c2dkTVVZT29sTng1a0tZL01RekNrRy9aM0pYT0NoS1ZMQW96OHVnK0o0bGhRQnNqTitFdkozTHNOZitYMVZoNDBGZjJCbHgxOUxwY0ZSRTRPckR1ekU3NXNYajYvNndNbE1HV0JJTFZFTytIUE9zMVVqdWhpT01DT2p2N1RtQmNSaGM5cG5rPS0tamlPSTJkR2NUejR3anY5a2VKLzNQQT09--894c463f7c61d697a0606a1594a4e31064859d75"
base_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Host": "ais.usvisa-info.com",
    # Security
    "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
}

USERNAME = config['USVISA']['USERNAME']
PASSWORD = config['USVISA']['PASSWORD']
SCHEDULE_ID = config['USVISA']['SCHEDULE_ID']
MY_SCHEDULE_DATE = config['USVISA']['MY_SCHEDULE_DATE']
COUNTRY_CODE = config['USVISA']['COUNTRY_CODE']
FACILITY_ID = config['USVISA']['FACILITY_ID']

SENDGRID_API_KEY = config['SENDGRID']['SENDGRID_API_KEY']
PUSH_TOKEN = config['PUSHOVER']['PUSH_TOKEN']
PUSH_USER = config['PUSHOVER']['PUSH_USER']

LOCAL_USE = config['CHROMEDRIVER'].getboolean('LOCAL_USE')
HUB_ADDRESS = config['CHROMEDRIVER']['HUB_ADDRESS']

REGEX_CONTINUE = "//a[contains(text(),'Continue')]"


STEP_TIME = 0.5  # time between steps (interactions with forms): 0.5 seconds
RETRY_TIME = random.randint(70, 90)  # wait time between retries/checks for available dates: 10 minutes
# RETRY_TIME = 60*10  # wait time between retries/checks for available dates: 10 minutes
EXCEPTION_TIME = 60*30  # wait time when an exception occurs: 30 minutes
COOLDOWN_TIME = 60*60  # wait time when temporary banned (empty list): 60 minutes

DATE_URL = f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/schedule/{SCHEDULE_ID}/appointment/days/{FACILITY_ID}.json?appointments[expedite]=false"
TIME_URL = f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/schedule/{SCHEDULE_ID}/appointment/times/{FACILITY_ID}.json?date=%s&appointments[expedite]=false"
APPOINTMENT_URL = f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/schedule/{SCHEDULE_ID}/appointment"
EXIT = False
