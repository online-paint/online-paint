from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from Client import send_keyboard_action

class Keyboard(BoxLayout):
    def __init__(self, filename_input, **kwargs):
        super().__init__(**kwargs)
        self.filename_input = filename_input
        self.orientation = 'vertical'
        self.padding = [10, 10, 10, 15]
        self.spacing = 7
        self.size_hint_x = 1
        self.size_hint_y = None
        self.height = 400
        self.create_keyboard()

    def create_keyboard(self):
        rows = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Back'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Space', '_', '.'],
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
        ]
        
        for row in rows:
            row_layout = BoxLayout(size_hint_x = 1, size_hint_y=0.2, spacing = 7)
            for key in row:
                button = Button(text=key, size_hint_x=0.1)
                button.bind(on_press=self.on_key_press)
                row_layout.add_widget(button)
            self.add_widget(row_layout)

    def on_key_press(self, instance):
        key = instance.text
        send_keyboard_action(key)
        if key == 'Back':
            self.filename_input.text = self.filename_input.text[:-1]
        elif key == 'Space':
            self.filename_input.text += ' '
        else:
            self.filename_input.text += key
