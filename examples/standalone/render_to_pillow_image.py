from PIL import Image
import ModernGL, struct

size = 500, 500
ctx = ModernGL.create_standalone_context()

color_rbo = ctx.Renderbuffer(size)
depth_rbo = ctx.DepthRenderbuffer(size)
fbo = ctx.Framebuffer([color_rbo, depth_rbo])
# fbo = ctx.Framebuffer([color_rbo])
fbo.use()

prog = ctx.program([
	ctx.vertex_shader('''
		#version 330

		in vec2 vert;
		out vec2 tex;

		void main() {
			gl_Position = vec4(vert, 0.0, 1.0);
			tex = vert / 2.0;
		}
	'''),
	ctx.fragment_shader('''
		#version 330

		in vec2 tex;
		out vec4 color;

		void main() {
			vec2 z = tex;

			int i;
			for(i = 0; i < 100; i++) {
				vec2 v = vec2((z.x * z.x - z.y * z.y), (z.y * z.x + z.x * z.y)) - vec2(0.64, -0.47);
				if (dot(v, v) > 4.0) break;
				z = v;
			}

			float cm = fract((i == 100 ? 0.0 : float(i)) * 10.0 / 100);
			color = vec4(fract(cm + 0.0 / 3.0), fract(cm + 1.0 / 3.0), fract(cm + 2.0 / 3.0), 1.0);
		}
	''')
])

vbo = ctx.buffer(struct.pack('8f', -1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0))
vao = ctx.simple_vertex_array(prog, vbo, ['vert'])

ctx.viewport = (0, 0, size[0], size[1])
vao.render(ModernGL.TRIANGLE_STRIP)

img = Image.frombytes('RGBA', size, fbo.read(size)).transpose(Image.FLIP_TOP_BOTTOM)
img.save('T:/Fractal.png')