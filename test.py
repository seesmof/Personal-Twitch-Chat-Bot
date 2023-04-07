import pyautogui
import pygetwindow as gw

# Display the alert
pyautogui.alert('This is an alert', "Check Chat!", timeout=None)

# Find the alert window and bring it to the front
alert_window = gw.getWindowsWithTitle('Чуваче, диви чат!')[0]
alert_window.activate()
