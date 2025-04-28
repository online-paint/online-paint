from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle


class ServerPaintCanvas(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = 1
        self.size_hint_y = None
        self.height = 1000
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_background, pos=self.update_background)
        self.line_color = (0, 0, 0, 1)
        self.drawing_line = None

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def create_line(self, touch_x, touch_y, color_1, color_2, color_3, color_4):
        with self.canvas:
            self.line_color = (color_1, color_2, color_3, color_4)
            Color(*self.line_color)
            self.drawing_line = Line(points=(touch_x, touch_y), width=4)

    def simulate_touch_down(self, touch_x, touch_y, color_1, color_2, color_3, color_4):
        with self.canvas:
            self.create_line(touch_x, touch_y, color_1, color_2, color_3, color_4)

    def simulate_touch_move(self, touch_x, touch_y, color_1, color_2, color_3, color_4):
        if self.drawing_line is not None:
            self.drawing_line.points += [touch_x, touch_y]
        else:
            self.create_line(touch_x, touch_y, color_1, color_2, color_3, color_4)

    def simulate_touch_up(self):
        self.drawing_line = None
        return

    def clear_canvas(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def paint(self, touch_x, touch_y, color_1, color_2, color_3, color_4, mode: int):
        if (mode == 0):
            self.simulate_touch_down(touch_x, touch_y, color_1, color_2, color_3, color_4)
        if (mode == 1):
            self.simulate_touch_move(touch_x, touch_y, color_1, color_2, color_3, color_4)
        if (mode == 2):
            self.simulate_touch_up()