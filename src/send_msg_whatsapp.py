import webbrowser
import pyautogui
import time

DATA_FOLDER = "../data"
dark_mode = f"{DATA_FOLDER}/attachments.png"
light_mode = f"{DATA_FOLDER}/attachments_light.png"
wait_img = f"{DATA_FOLDER}/not_sent.png"


def wait_for_sent():
    """
    it searches for not sent icon on screen if it is not present then it moves on
    :return: True
    """
    location = pyautogui.locateOnScreen(wait_img)
    while location is not None:
        location = pyautogui.locateOnScreen(wait_img)
    return True


def send_message(number, message):
    """
    sends messages to whatsapp using whatsapp web
    :param number: phone number of client
    :param message: message to be sent
    :return:
    """
    webbrowser.open_new_tab(
        f"https://web.whatsapp.com/send?phone={number}&text={message}"
    )
    location = pyautogui.locateOnScreen(dark_mode) or pyautogui.locateOnScreen(light_mode)
    while location is None:
        location = pyautogui.locateOnScreen(dark_mode) or pyautogui.locateOnScreen(light_mode)
    pyautogui.press("Enter")
    wait_for_sent()
    pyautogui.hotkey("ctrl", "w")
