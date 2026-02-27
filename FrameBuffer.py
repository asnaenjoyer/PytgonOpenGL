import moderngl
import glfw
import numpy as np

class FrameBuffer:
    def __init__(self, ctx, width, height, post_program):
        self.ctx = ctx
        self.width = width
        self.height = height
        self.post_program = post_program

        self.color_tex = ctx.texture((width, height), 4)
        self.depth_rb = ctx.depth_renderbuffer((width, height))
        self.fbo = ctx.framebuffer(color_attachments=[self.color_tex], depth_attachment=self.depth_rb)

        quad_vertices = np.array([
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
             1.0,  1.0, 1.0, 1.0,
            -1.0, -1.0, 0.0, 0.0,
             1.0,  1.0, 1.0, 1.0,
            -1.0,  1.0, 0.0, 1.0,
        ], dtype='f4')

        self.quad_vbo = ctx.buffer(quad_vertices.tobytes())
        self.quad_vao = ctx.vertex_array(
            post_program,
            [(self.quad_vbo, '2f 2f', 'in_pos', 'in_uv')]
        )

    def use(self):
        self.fbo.use()
        self.ctx.clear(0.0, 0.0, 0.0, 0.0)

    def render_to_screen(self):
        self.ctx.screen.use()
        if 'time' in self.post_program:
            self.post_program['time'].value = glfw.get_time()
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        self.color_tex.use(0)
        self.quad_vao.render()

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.color_tex.release()
        self.depth_rb.release()
        self.color_tex = self.ctx.texture((width, height), 4)
        self.depth_rb = self.ctx.depth_renderbuffer((width, height))
        self.fbo = self.ctx.framebuffer(color_attachments=[self.color_tex], depth_attachment=self.depth_rb)