from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from PaintCanvas import PaintCanvas
from Keyboard import Keyboard

class PaintApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', spacing = 0)
        Window.size = (1000, 800)
        
        # Top Bar
        top_bar = BoxLayout(size_hint_x = 1, size_hint_y = None, height = 100, padding=[10, 10, 10, 0], spacing = 10)
        
        # Filename
        self.filename_input = TextInput(hint_text="Enter filename", size_hint=(0.6, 1))
        self.filename_input.padding = [25, 25]
        top_bar.add_widget(self.filename_input)

        # Save Button
        save_btn = Button(text="Save", size_hint=(0.12, 1))
        save_btn.bind(on_press=self.save_canvas)
        top_bar.add_widget(save_btn)

        # Exit Button
        exit_btn = Button(text="Exit", size_hint=(0.12, 1))
        exit_btn.bind(on_press=self.stop_app)
        top_bar.add_widget(exit_btn)

        main_layout.add_widget(top_bar)
        
        # Keyboard
        keyboard_layout = Keyboard(filename_input=self.filename_input)
        main_layout.add_widget(keyboard_layout)

        # Canvas area
        self.canvas_widget = PaintCanvas()
        main_layout.add_widget(self.canvas_widget)

        # Control Bar
        controls_layout = BoxLayout(size_hint_x = 1, size_hint_y = None, height = 100, padding=[10, 12], spacing=10)
        
        # Color Buttons
        buttons_layout = BoxLayout(size_hint=(0.7, 1), spacing=15)
        buttons_layout.padding = [10, 10, 400, 10]
        self.color_buttons = {}
        colors = [((240/255, 40/255, 40/255, 1), 'Red'), ((80/255, 249/255, 131/255, 1), 'Green'), ((54/255, 64/255, 244/255, 1), 'Blue'), ((247/255, 242/255, 25/255, 1), 'Yellow'), ((50/255, 50/255, 50/255, 1), 'Black')]
        for color, label in colors:
            btn = ToggleButton(group="colors", background_normal="", background_color=color, size_hint=(0.2, 1), outline_color=(1, 1, 1, 1), outline_width=4)
            btn.bind(on_press=lambda instance, c=color: self.set_color_and_select(c, instance))
            buttons_layout.add_widget(btn)
            self.color_buttons[btn] = color 
        controls_layout.add_widget(buttons_layout)
        
        for btn, color in self.color_buttons.items():
            if color == (0, 0, 0, 1):
                btn.state = 'down'
                break

        #Pen and Eraser
        pen_btn = Button(text="Pen", size_hint=(0.15, 1))
        def activate_pen(instance):
            self.canvas_widget.set_eraser_mode(False)
        pen_btn.bind(on_press=activate_pen)
        controls_layout.add_widget(pen_btn)

        eraser_btn = Button(text="Eraser", size_hint=(0.15, 1))
        def activate_eraser(instance):
            self.canvas_widget.set_eraser_mode(True)
            eraser_btn.state = 'down'
        eraser_btn.bind(on_press=activate_eraser)
        controls_layout.add_widget(eraser_btn)

        # Clear button
        clear_btn = Button(text="Clear", size_hint=(0.15, 1))
        clear_btn.bind(on_press=lambda instance: self.canvas_widget.clear_canvas()) 
        controls_layout.add_widget(clear_btn)

        main_layout.add_widget(controls_layout)

        return main_layout
    
    def set_color_and_select(self, color, button):
        self.canvas_widget.set_color(color)
        for btn in self.color_buttons.keys():
            btn.state = 'normal'
        button.state = 'down'

    def save_canvas(self, instance):
        filename = self.filename_input.text.strip()
        if filename:
            self.canvas_widget.export_to_png(filename + ".png")

    def stop_app(self, instance):
        App.get_running_app().stop()