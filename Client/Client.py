import socket

def run_client():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = input("Enter Server IP: ")
    server_port = 8000
    client.connect((server_ip, server_port))
    send_clear()
    
def send_close():
    msg = "close"
    client.send(msg.encode("utf-8")[:1024])
    client.recv(1024)

def send_clear():
    msg = "clear"
    client.send(msg.encode("utf-8")[:1024])
    client.recv(1024)
    
def send_paint(touch_x, touch_y, line_color, mode):
    color1, color2, color3, color4 = line_color
    msg = f"paint {touch_x} {touch_y} {color1} {color2} {color3} {color4} {mode}"
    client.send(msg.encode("utf-8")[:1024])
    client.recv(1024)

def send_keyboard_action(key):
    msg = f"keyboard {key}"
    client.send(msg.encode("utf-8")[:1024])
    client.recv(1024)
