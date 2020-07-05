import PySimpleGUI as sg
import myclient
import sys

def make_dpi_aware():
    import ctypes
    import platform
    if int(platform.release()) >= 8:
         ctypes.windll.shcore.SetProcessDpiAwareness(True)
         
make_dpi_aware()

layout = [[sg.Multiline(size=(45, 20), disabled=True, key="BOX", autoscroll=True)],
          [sg.Input(key="INPUT"), sg.Button("SEND", key="SEND", bind_return_key=True)],
          [sg.Button("Exit")]]

window = sg.Window("Extremely Simple Chat App", layout, keep_on_top=True)

client = myclient.MyClient()
if not client.connected:
    sg.popup("Could not connect to the server. Start the server first.")
    sys.exit()
client.start_reciever()

while True:  # Event Loop
    event, values = window.read(timeout=100)
    # print(event, values)
    if event in (sg.WIN_CLOSED, "Exit", None):
        client.send(myclient.DISCONNECT_MESSAGE)
        break
    if event == "SEND":
        msg = values["INPUT"]
        window["INPUT"].Update(value="")
        
        client.send(msg)
    
    window["BOX"].Update(value="\n".join(client.history))

window.close()
