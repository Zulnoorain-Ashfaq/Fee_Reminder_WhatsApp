# Fee_Reminder_WhatsApp

This project is a Python script that sends a fee reminder on WhatsApp to the numbers of clients.

## Files

* `not_sent.png` : image of the clock which appears when msg is still sending
* `attachments.png` : image of attachment icon on whatsapp web in dark mode
* `attachments_light.png` : image of attachment icon on whatsapp web in light mode
* `information.json` : contains the message to be sent to clients and also admin's phone number
* `monthly_fee_record.xlsx` : it contains all data. new col must be added in the format june 2023 in excel
* `reminder.json` : it contains data about the last date on which the fee reminder was sent to clients

## How To Use

1. first login to whatsapp web on the browser.
2. take screenshots of attachments icon in the chat in either light mode or dark mode
   and also take screenshot of the not_sent clock
3. update information.json file according to your needs
4. provide data in the given format
5. run the fee_reminder.py

