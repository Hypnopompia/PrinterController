import pygame


class Component:
    def __init__(self, x, y, width, height):

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.move_steps = None

        self.move_x_speed = None
        self.move_x_tween = None
        self.move_x_start = self.x
        self.move_x_target = self.x
        self.move_x_steps = 0
        self.move_x_distance = None
        self.move_x_direction = None
        self.move_x_step = 0

        self.move_y_speed = None
        self.move_y_tween = None
        self.move_y_start = self.y
        self.move_y_target = self.y
        self.move_y_steps = 0
        self.move_y_distance = None
        self.move_y_direction = None
        self.move_y_step = 0

    def aspect_scale(self, img, bx, by):
        """ Scales 'img' to fit into box bx/by.
         This method will retain the original image's aspect ratio """
        ix, iy = img.get_size()
        if ix > iy:
            # fit to width
            scale_factor = bx / float(ix)
            sy = scale_factor * iy
            if sy > by:
                scale_factor = by / float(iy)
                sx = scale_factor * ix
                sy = by
            else:
                sx = bx
        else:
            # fit to height
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            if sx > bx:
                scale_factor = bx / float(ix)
                sx = bx
                sy = scale_factor * iy
            else:
                sy = by

        return pygame.transform.scale(img, (int(sx), int(sy)))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_moving(self):
        if self.move_x_target != self.x or self.move_y_target != self.y:
            return True
        else:
            return False

    def move_to(self, x, y, x_speed=None, y_speed=None, x_tween=None, y_tween=None):
        if x_speed is None and y_speed is None:
            self.x = x
            self.y = y
            return

        self.move_x_speed = x_speed
        self.move_x_tween = x_tween

        self.move_y_speed = y_speed
        self.move_y_tween = y_tween

        if self.x != x:
            self.move_x_start = self.x
            self.move_x_target = x
            self.move_x_direction = 1 if self.move_x_target > self.x else -1
            self.move_x_distance = abs(self.move_x_target - self.x)
            self.move_x_steps = abs(self.x - self.move_x_target) // self.move_x_speed

        if self.y != y:
            self.move_y_start = self.y
            self.move_y_target = y
            self.move_y_direction = 1 if self.move_y_target > self.y else -1
            self.move_y_distance = abs(self.move_y_target - self.y)
            self.move_y_steps = abs(self.y - self.move_y_target) // self.move_y_speed

        self.move_steps = max(self.move_x_steps, self.move_y_steps)
        self.move_x_step = 0 if self.move_x_direction == 1 else self.move_steps
        self.move_y_step = 0 if self.move_y_direction == 1 else self.move_steps

    def animate(self):
        if self.move_x_target != self.x:
            x_perc = self.move_x_tween(max(0, min(1.0, (self.move_x_step / self.move_steps))))
            self.x = int(self.move_x_distance * x_perc) + min(self.move_x_start, self.move_x_target)
            self.move_x_step += self.move_x_direction

            if self.move_x_step > self.move_steps or self.move_x_step < 0:
                self.x = self.move_x_target

        if self.move_y_target != self.y:
            y_perc = self.move_y_tween(max(0, min(1.0, (self.move_y_step / self.move_steps))))
            self.y = int(self.move_y_distance * y_perc) + min(self.move_y_start, self.move_y_target)
            self.move_y_step += self.move_y_direction

            if self.move_y_step >= self.move_steps or self.move_y_step <= 0:
                self.y = self.move_y_target

    def process_event(self, event):
        raise NotImplementedError()

    def update(self, state):
        raise NotImplementedError()

    def render(self, surface):
        raise NotImplementedError()
