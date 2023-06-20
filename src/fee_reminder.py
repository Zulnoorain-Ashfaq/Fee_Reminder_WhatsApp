from send_msg_whatsapp import send_message
import json
import pandas as pd
import time
from datetime import date


DATA_FOLDER = "../data"

info = json.load(open(f"{DATA_FOLDER}/information.json"))
MSG = info["message"]
PERSONAL_NUMBER = info["personal_number"]

data = pd.read_excel(f"{DATA_FOLDER}/monthly_fee_record.xlsx")

# setting col name to only date excluding the time
cols = list(data.columns)
for col in range(4, len(cols)):
    cols[col] = str(cols[col].date())
data.columns = cols

# filtering data to get client to whom reminder is to be sent
data = data[data["Fee Reminder"] == "yes"]


def last_date_cal(row):
    """
    it gets the last date on which client paid the fee
    :param row: df row
    :return: last month
    """
    last = row.dropna()
    label = last.index[-1]
    day = f"{int(row[2]):02}"
    last_label = label[:8] + day
    return last_label


def last_fee_cal(row):
    """
    it gets the last fee which client paid
    :param row: row of df after adding the last payment col
    :return:
    """
    last = row.dropna()
    fee = last[-2]
    return fee

# adding new info
data["last_payment"] = data.apply(last_date_cal, axis=1)
data["last_fee"] = data.apply(last_fee_cal, axis=1)

# getting current date info
current_date = date.today()
current_day = current_date.day
current_year = current_date.year
current_month = current_date.month
current_total_days = current_year * 365 + current_month * 30 + current_day

# calculating total days from start to the date client last paid
data["total_days"] = data.last_payment.apply(
    lambda x: int(x[0:4]) * 365 + int(x[5:7]) * 30 + int(x[8:])
)
# subtracting last client total days from current total days to get the days from last fee submission
data["days_from_last_submission"] = data.total_days.apply(
    lambda x: current_total_days - x
)

# filtering clients who have days from last submission more than or equal to 30 i.e their due date
defaulters = data[data.days_from_last_submission >= 30]

# getting the reminder info from file
# it contains the last date on which fee reminder was sent to the person
JSON_PATH = f"{DATA_FOLDER}/reminder.json"
reminder_info = json.load(open(JSON_PATH, "r"))

# filtered defaulters
reminder_list = {}
for index, defaulter in defaulters.iterrows():
    if defaulter["name"] in reminder_info:
        if date.today().__str__() == reminder_info[defaulter["name"]]:
            continue
        else:
            reminder_list[defaulter["name"]] = defaulter["numbers"].replace("\xa0", "")
    else:
        reminder_list[defaulter["name"]] = defaulter["numbers"].replace("\xa0", "")
    # updating the reminder dictionary(json)
    reminder_info[defaulter["name"]] = date.today().__str__()

# sending messages to whatsapp
for name, number in reminder_list.items():
    time.sleep(.5)
    send_message(number, MSG)

# sending special msg sontaining all info of clients to the admin
if reminder_info["ADMIN"] != date.today().__str__():
    special_msg = ""
    for index, defaulter in defaulters.iterrows():
        special_msg += f'name: {defaulter["name"]}\nFee: {defaulter["last_fee"]}\nLast date:{defaulter["last_payment"]}\ndays since last submission: {defaulter["days_from_last_submission"]}\n--------------------------------\n'
    new_msg = ''
    for m in special_msg.split("\n"):
        new_msg += m.ljust(150)

    send_message(PERSONAL_NUMBER, special_msg)
    reminder_info["ADMIN"] = date.today().__str__()

# updating the json file
json.dump(reminder_info, open(JSON_PATH, "w"))
