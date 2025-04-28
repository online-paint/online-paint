from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from Client import send_paint, send_clear

class PaintCanvas(Widget):
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
        self.eraser_mode = False
        self.drawine_line = None

    def update_background(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
        
    def create_line(self, touch_x, touch_y):
        with self.canvas:
            Color(*self.line_color)
            self.drawine_line = Line(points=(touch_x, touch_y), width=4)

    def on_touch_down(self, touch):
        if not self.collide_point(touch.x, touch.y):
            return False
        send_paint(touch.x, touch.y, self.line_color, 0)
    
        with self.canvas:
            self.create_line(touch.x, touch.y)

    def on_touch_move(self, touch):
        if not self.collide_point(touch.x, touch.y):
            self.drawine_line = None
            send_paint(touch.x, touch.y, self.line_color, 2)
            return False
        send_paint(touch.x, touch.y, self.line_color, 1)
    
        if self.drawine_line != None:
            self.drawine_line.points += [touch.x, touch.y]
        else:
            self.create_line(touch.x, touch.y)
    
    def on_touch_up(self, touch):
        send_paint(touch.x, touch.y, self.line_color, 2)
        self.drawine_line = None
        return

    def clear_canvas(self):
        send_clear()
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def set_color(self, color):
        self.line_color = color

    def set_eraser_mode(self, mode):
        self.eraser_mode = mode
        if self.eraser_mode:
            self.line_color = (1, 1, 1, 1)
        else:
            self.line_color = (0, 0, 0, 1)