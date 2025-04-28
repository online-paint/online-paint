from kivy.clock import Clock
from threading import Thread
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from ServerPaintCanvas import ServerPaintCanvas



def paint_app_instance(conn):

    class ServerPaintApp(App):
        def build(self):
            main_layout = BoxLayout(orientation='vertical', spacing=0)
            Window.size = (1000, 800)

            top_bar_placeholder = BoxLayout(size_hint_x=1, size_hint_y=None, height=500)
            self.name_label = Label()
            self.name_label.color = (1, 1, 1, 1)
            self.name_label.font_size = 100
            top_bar_placeholder.add_widget(self.name_label)
            main_layout.add_widget(top_bar_placeholder)

            self.canvas_widget = ServerPaintCanvas()
            main_layout.add_widget(self.canvas_widget)

            controls_layout_placeholder = BoxLayout(size_hint_x=1, size_hint_y=None, height=100, padding=[10, 12],
                                                    spacing=10)
            main_layout.add_widget(controls_layout_placeholder)

            return main_layout

        def stop_app(self):
            App.get_running_app().stop()

        def update_name(self, key):
            if key == 'Back':
                self.name_label.text = self.name_label.text[:-1]
            elif key == 'Space':
                self.name_label.text += ' '
            else:
                self.name_label.text += key

        def on_start(self):

            def listen_for_commands():
                while True:
                    command = conn.recv()
                    print(f"Received command: {command}")
                    if command == "clear":
                        Clock.schedule_once(lambda dt: self.canvas_widget.clear_canvas())
                    elif command.startswith("keyboard"):
                        _, key = command.split()
                        Clock.schedule_once(lambda dt: self.update_name(key))
                    elif command.startswith("paint"):
                        _, touch_x_str, touch_y_str, color1_str, color2_str, color3_str, color4_str, mode_str = command.split()
                        color1 = float(color1_str)
                        color2 = float(color2_str)
                        color3 = float(color3_str)
                        color4 = float(color4_str)
                        mode = int(mode_str)
                        touch_x = float(touch_x_str)
                        touch_y = float(touch_y_str)
                        Clock.schedule_once(lambda dt: self.canvas_widget.paint(touch_x, touch_y, color1, color2, color3, color4, mode))
                    elif command == "close":
                        Clock.schedule_once(lambda dt: self.stop_app())

            Thread(target=listen_for_commands, daemon=True).start()

    ServerPaintApp().run()