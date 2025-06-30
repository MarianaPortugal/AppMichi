from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.graphics import PushMatrix, PopMatrix, Scale, Translate

class ScalableImage(Image):
    scale = NumericProperty(1.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(scale=self.update_transform)
        self.bind(pos=self.update_transform, size=self.update_transform)
        with self.canvas.before:
            self._push = PushMatrix()
            self._translate = Translate(0, 0, 0)
            self._scale = Scale(1.0, 1.0, 1.0)
        with self.canvas.after:
            self._pop = PopMatrix()
        self.update_transform()

    def update_transform(self, *args):
        cx, cy = self.center
        self._translate.xy = (cx * (1 - self.scale), cy * (1 - self.scale))
        self._scale.xyz = (self.scale, self.scale, 1)

