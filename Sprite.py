import moderngl
import numpy as np
from pyrr import Matrix44
from PIL import Image


class Sprite:
    def __init__(self, ctx, program, texture_path, position=(0, 0), size=(100, 100), rotation=0, name="SpriteDefault"):
        self.ctx = ctx
        self.program = program

        self.position = np.array(position, dtype='f4')
        self.size = np.array(size, dtype='f4')
        self.rotation = rotation

        vertices = np.array([
            -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, 1.0, 0.0,
             0.5,  0.5, 1.0, 1.0,

            -0.5, -0.5, 0.0, 0.0,
             0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5, 0.0, 1.0,
        ], dtype='f4')

        self.vbo = ctx.buffer(vertices.tobytes())
        self.vao = ctx.vertex_array(
            program,
            [(self.vbo, '2f 2f', 'in_pos', 'in_uv')]
        )

        self.texture = self.load_texture(texture_path)
        self.name = name

    def load_texture(self, path):
        img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        texture = self.ctx.texture(img.size, 4, img.convert('RGBA').tobytes())
        texture.build_mipmaps()
        texture.use()
        return texture

    def get_model_matrix(self):
        model = Matrix44.identity()

        model *= Matrix44.from_translation([self.position[0], self.position[1], 0.0])
        model *= Matrix44.from_z_rotation(self.rotation)
        model *= Matrix44.from_scale([self.size[0], self.size[1], 1.0])

        return model.astype('f4')

    def draw(self, projection):
        self.texture.use()
        self.program['model'].write(self.get_model_matrix())
        self.program['projection'].write(projection.astype('f4'))
        self.vao.render()


class SpriteGroup:
    def __init__(self, ctx, program):
        self.ctx = ctx
        self.program = program
        self.sprites = []

        quad_vertices = np.array([
            -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, 1.0, 0.0,
             0.5,  0.5, 1.0, 1.0,
            -0.5, -0.5, 0.0, 0.0,
             0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5, 0.0, 1.0,
        ], dtype='f4')

        self.vbo = ctx.buffer(quad_vertices.tobytes())
        self.vao = ctx.vertex_array(program, [(self.vbo, '2f 2f', 'in_pos','in_uv')])

    def __iter__(self):
        return iter(self.sprites)

    def add(self, sprite):
        self.sprites.append(sprite)

    def remove(self, sprite):
        self.sprites.remove(sprite)

    def draw(self, projection):
        self.program['projection'].write(projection.astype('f4'))
        for sprite in self.sprites:
            sprite.texture.use()
            self.program['model'].write(sprite.get_model_matrix())
            self.vao.render()