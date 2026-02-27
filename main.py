import glfw
from utils import *
from App import Game
from Sprite import Sprite, SpriteGroup
from test.world import World


class MyMiniGame(Game):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.world_program = self.ctx.program(
            vertex_shader=load_shader("shaders/test/world.vert"),
            fragment_shader=load_shader("shaders/test/world.frag")
        )
        self.world = World(2000, 2000, self.ctx, self.world_program, (0,0))

    def draw(self):
        self.world.draw(self.projection)
        

    def update(self):
        if self.is_mouse_pressed():
            m_pos_x, m_pos_y = self.screen_to_world()
            dx = m_pos_x - self.width / 2
            dy = m_pos_y - self.height / 2
            self.set_camera_pos(self.camera_pos[0] + (dx * self.delta_time), self.camera_pos[1] + (dy * self.delta_time))

        self.world_program['view'].write(self.get_view_matrix().astype("f4"))


if __name__ == "__main__":
    game = MyMiniGame(720, 720)
    game.mainloop()