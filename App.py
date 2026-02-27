
import glfw
import moderngl
import numpy as np
from pyrr import Matrix44
from PIL import Image
import math
import time

from Sprite import Sprite, SpriteGroup
from FrameBuffer import FrameBuffer
from utils import load_shader

class App:
    def __init__(self, width, height, title="ModernGL App"):
        self.width, self.height = width, height

        if not glfw.init():
            raise Exception("GLFW init failed")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(self.width, self.height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window creation failed")

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        glfw.set_window_size_callback(self.window, self.on_resize)

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        self.projection = None
        self.fbo = None

        self.delta_time = 0.0
        self._last_time = glfw.get_time()

        self.m_pos_x = 0
        self.m_pos_y = 0

    def mainloop(self):
        while not glfw.window_should_close(self.window):
            current_time = glfw.get_time()
            self.delta_time = current_time - self._last_time
            self._last_time = current_time

            glfw.poll_events()

            self.m_pos_x, self.m_pos_y = glfw.get_cursor_pos(self.window)

            self.pre_draw()
            self.draw()
            self.post_draw()

            glfw.swap_buffers(self.window)
            self.update()

        glfw.terminate()

    def pre_draw(self):
        pass

    def draw(self):
        pass

    def post_draw(self):
        pass

    def update(self):
        pass

    def on_resize(self, window, width, height):
        self.width, self.height = width, height
        self.ctx.viewport = (0, 0, width, height)

    def screen_to_world(self):
        return self.m_pos_x, self.height - self.m_pos_y
    
    def is_mouse_pressed(self, button=glfw.MOUSE_BUTTON_LEFT):
        return glfw.get_mouse_button(self.window, button) == glfw.PRESS

class Game(App):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.program = self.ctx.program(
            vertex_shader=load_shader("shaders/sprite.vert"),
            fragment_shader=load_shader("shaders/sprite.frag")
        )

        self.post_program = self.ctx.program(
            vertex_shader=load_shader("shaders/post.vert"),
            fragment_shader=load_shader("shaders/post.frag")
        )

        self.projection = Matrix44.orthogonal_projection(0, self.width, 0, self.height, -1, 1)
        

        self.fbo = FrameBuffer(self.ctx, self.width, self.height, self.post_program)

        self.camera_pos = np.array([0.0, 0.0])
        self.zoom = 1.0
        self.program["view"].write(self.get_view_matrix().astype("f4"))

    def pre_draw(self):
        self.fbo.use()

    def draw(self):
        pass

    def post_draw(self):
        self.fbo.render_to_screen()

    def update(self):
        pass

    def on_resize(self, window, width, height):
        super().on_resize(window, width, height)
        self.fbo.resize(width, height)
        self.projection = Matrix44.orthogonal_projection(0, width, 0, height, -1, 1)

    def get_view_matrix(self):
        translation = Matrix44.from_translation((-self.camera_pos[0], -self.camera_pos[1], 0.0))
        scaling = Matrix44.from_scale([self.zoom, self.zoom, 1.0])
        return scaling @ translation
    
    def set_camera_pos(self, x, y):
        self.camera_pos = np.array([x, y])
        self.program["view"].write(self.get_view_matrix().astype("f4"))

    def set_zoom(self, zoom_factor):
        self.zoom = zoom_factor
        self.program["view"].write(self.get_view_matrix().astype("f4"))
        