
import pyglet
from pyglet.gl import *
from pyglet import image

from shader import *
from math3d import *


cubeBuffer = [
				-1.0, 1.0, -1.0,	0.4, 0.4, 0.4,		-1.0, 1.0, 1.0,		0.4, 0.4, 0.4,		 1.0, 1.0, 1.0,		0.4, 0.4, 0.4,
				-1.0, 1.0, -1.0,	0.4, 0.4, 0.4,		 1.0, 1.0, 1.0,		0.4, 0.4, 0.4,		 1.0, 1.0, -1.0,	0.4, 0.4, 0.4,

				1.0, -1.0, -1.0,	0.8, 0.8, 0.8,		 1.0, -1.0, 1.0,	0.8, 0.8, 0.8,		-1.0, -1.0, 1.0,	0.8, 0.8, 0.8,
				1.0, -1.0, -1.0,	0.8, 0.8, 0.8,		-1.0, -1.0, 1.0,	0.8, 0.8, 0.8,		-1.0, -1.0, -1,		0.8, 0.8, 0.8,

				-1.0, -1.0, -1,		1.0, 0.0, 0.0,		-1.0, -1.0, 1.0,	1.0, 0.0, 0.0,		-1.0, 1.0, 1.0,		1.0, 0.0, 0.0,
				-1.0, -1.0, -1,		1.0, 0.0, 0.0,		-1.0, 1.0, 1.0,		1.0, 0.0, 0.0,		-1.0, 1.0, -1.0,	1.0, 0.0, 0.0,

				1.0, -1.0, 1.0,		0.0, 1.0, 0.0, 		 1.0, -1.0, -1.0,	0.0, 1.0, 0.0, 		 1.0, 1.0, -1.0,	0.0, 1.0, 0.0,
				1.0, -1.0, 1.0,		0.0, 1.0, 0.0, 		 1.0, 1.0, -1.0,	0.0, 1.0, 0.0, 		 1.0, 1.0, 1.0,		0.0, 1.0, 0.0,

				1.0, 1.0, -1.0,		0.0, 0.0, 1.0, 		 1.0, -1.0, -1.0,	0.0, 0.0, 1.0,		-1.0, -1.0, -1,		0.0, 0.0, 1.0,
				1.0, 1.0, -1.0,		0.0, 0.0, 1.0, 		-1.0, -1.0, -1,		0.0, 0.0, 1.0,		-1.0, 1.0, -1.0,	0.0, 0.0, 1.0,

				-1.0, -1.0, 1.0,	1.0, 1.0, 0.0, 		 1.0, -1.0, 1.0,	1.0, 1.0, 0.0,		 1.0, 1.0, 1.0,		1.0, 1.0, 0.0,
				-1.0, -1.0, 1.0,	1.0, 1.0, 0.0,		 1.0, 1.0, 1.0,		1.0, 1.0, 0.0,		-1.0, 1.0, 1.0,		1.0, 1.0, 0.0,
			]


GL_ELEMENT_ARRAY_BUFFER = 34963

width = 800
height = 600

window = pyglet.window.Window(width=width, height=height)

vboId = GLuint()

vboBuffer = (GLfloat * len(cubeBuffer))(*cubeBuffer)

myShader = Shader(''.join(open('color.v.glsl')),''.join(open('color.f.glsl')))

myTime = 0
modelMatrix = identityMatrix
viewMatrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, -4, 1]
projMatrix = perspectiveGL(65.0, width / float(height), 1.0, 20.0)

def update(dt):
	global myTime, modelMatrix
	modelMatrix = rotMatrixY(myTime)
	myTime += 1

@window.event
def on_draw():
	glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

	myShader.bind()
	myShader.uniform_matrixf('modelMatrix', modelMatrix)
	myShader.uniform_matrixf('viewMatrix', viewMatrix)
	myShader.uniform_matrixf('projMatrix', projMatrix)

	glBindBuffer(GL_ARRAY_BUFFER, vboId)

	glEnableVertexAttribArray(0)
	glEnableVertexAttribArray(1)

	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, 0)
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, 12)

	glDrawArrays(GL_TRIANGLES, 0, len(vboBuffer) / 6)

	glDisableVertexAttribArray(0)
	glDisableVertexAttribArray(1)


glEnable(GL_DEPTH_TEST);
glClearColor(0.0, 0.0, 0.0, 1.0)

glGenBuffers(1, vboId)
glBindBuffer(GL_ARRAY_BUFFER, vboId)
glBufferData(GL_ARRAY_BUFFER, len(vboBuffer) * 4, vboBuffer, GL_STATIC_DRAW)

glViewport(0, 0, width, height)

TICKS_PER_SEC = 90
pyglet.clock.schedule_interval(update, 1.0 / TICKS_PER_SEC)

pyglet.app.run()
