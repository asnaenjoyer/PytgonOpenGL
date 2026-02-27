import numpy as np
from pyrr import Matrix44
from noise import pnoise2

CELL_SIZE = 4

class World:
    def __init__(self, rows, cols, ctx, program, position=(0,0), size=(1,1), rotation=0):
        self.rows = rows
        self.cols = cols
        self.program = program

        self.position = np.array(position, dtype='f4')
        self.size = np.array(size, dtype='f4')
        self.rotation = rotation

        self.vertices = []
        self.indices = []

        self.gen_mesh_only()
        
        
        vertices_array = np.array(self.vertices, dtype='f4')
        indices_array = np.array(self.indices, dtype='i4')

        self.vbo = ctx.buffer(vertices_array.tobytes())
        ibo = ctx.buffer(indices_array.tobytes())

        self.vao = ctx.vertex_array(
            program,
            [(self.vbo, '2f 1f', 'in_pos', 'in_color')],
            index_buffer=ibo
        )

    def get_model_matrix(self):
        model = Matrix44.identity()
        model *= Matrix44.from_translation([self.position[0], self.position[1], 0.0])
        model *= Matrix44.from_z_rotation(self.rotation)
        model *= Matrix44.from_scale([self.size[0], self.size[1], 1.0])
        return model.astype('f4')

    def draw(self, projection):
        self.program['model'].write(self.get_model_matrix())
        self.program['projection'].write(projection.astype('f4'))
        self.vao.render()

    def gen_mesh_only(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                
                scale = 0.025

                c = pnoise2(col * scale, row * scale, octaves=4)
                c = (c + 1) / 2 
                
                self.vertices.extend([
                    x, y, c,
                    x + CELL_SIZE, y, c,
                    x + CELL_SIZE, y + CELL_SIZE, c,
                    x, y + CELL_SIZE, c
                ])

        for row in range(self.rows):
            for col in range(self.cols):
                start = (row * self.cols + col) * 4
                self.indices.extend([
                    start, start+1, start+2,
                    start, start+2, start+3
                ])