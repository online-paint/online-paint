import kivy
from PaintApp import PaintApp
from Client import run_client
from Client import send_close

kivy.require("1.11.1")

if __name__ == "__main__":
    run_client()
    PaintApp().run()
    send_close()