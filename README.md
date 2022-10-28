# visa_rescheduler
US VISA (ais.usvisa-info.com) appointment re-scheduler

## Prerequisites
- Having a US VISA appointment scheduled already
- Google Chrome installed (to be controlled by the script)
- Python v3 installed (for running the script)
- API token from Pushover and/or a Sendgrid (for notifications)


## Initial Setup
- Create a `config.ini` file with all the details required (use config.ini.example)
- Install the required python packages: `pip3 install -r requirements.txt`

## Initial Setup
- SCHEDULE_ID -> initial schedule id from the url
- FACILITY_ID -> inspect element during scheduling to get for each location

## Executing the script
- Simply run `python3 visa.py`
- That's it!

## Acknowledgement
Thanks to @yaojialyu, @cejaramillof, @uxDaniel, @prajnamort, @yaoxiaoqi
https://gist.github.com/yaojialyu/0c59c23d84585cc6e889e394d928a164
https://github.com/uxDaniel/visa_rescheduler
https://github.com/prajnamort/visa_rescheduler
https://github.com/yaoxiaoqi/mew_rescheduler