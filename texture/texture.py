
import pyglet
from pyglet.gl import *
from pyglet import image

from shader import Shader
from math3d import *


cubeBuffer = [
				-1.0, 1.0, -1.0,	0,0,	-1.0, 1.0, 1.0,		1,0,	 1.0, 1.0, 1.0,		1,1,	
				-1.0, 1.0, -1.0,	0,0,	 1.0, 1.0, 1.0,		1,1,	 1.0, 1.0, -1.0,	0,1,
				
				1.0, -1.0, -1.0,	0,0,	 1.0, -1.0, 1.0,	1,0,	-1.0, -1.0, 1.0,	1,1,
				1.0, -1.0, -1.0,	0,0,	-1.0, -1.0, 1.0,	1,1,	-1.0, -1.0, -1,		0,1,
				
				-1.0, -1.0, -1,		0,0,	-1.0, -1.0, 1.0,	1,0,	-1.0, 1.0, 1.0,		1,1,
				-1.0, -1.0, -1,		0,0,	-1.0, 1.0, 1.0,		1,1,	-1.0, 1.0, -1.0,	0,1,
				
				1.0, -1.0, 1.0,		0,0,	 1.0, -1.0, -1.0,	1,0,	 1.0, 1.0, -1.0,	1,1,
				1.0, -1.0, 1.0,		0,0,	 1.0, 1.0, -1.0,	1,1,	 1.0, 1.0, 1.0,		0,1,
				
				1.0, 1.0, -1.0,		0,0,	 1.0, -1.0, -1.0,	1,0,	-1.0, -1.0, -1,		1,1,
				1.0, 1.0, -1.0,		0,0,	-1.0, -1.0, -1,		1,1,	-1.0, 1.0, -1.0,	0,1,
				
				-1.0, -1.0, 1.0,	0,0,	 1.0, -1.0, 1.0,	1,0,	 1.0, 1.0, 1.0,		1,1,
				-1.0, -1.0, 1.0,	0,0,	 1.0, 1.0, 1.0,		1,1,	-1.0, 1.0, 1.0,		0,1,
			]


GL_ELEMENT_ARRAY_BUFFER = 34963

width = 800
height = 600

window = pyglet.window.Window(width=width, height=height)
			
vboId = GLuint()

textureId = GLuint()
	
vboBuffer = (GLfloat * len(cubeBuffer))(*cubeBuffer)

myShader = Shader(''.join(open('texture.v.glsl')),''.join(open('texture.f.glsl')))

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
	
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, 0)
	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, 12)
	
	glDrawArrays(GL_TRIANGLES, 0, len(vboBuffer) / 5)
	
	glDisableVertexAttribArray(0)
	glDisableVertexAttribArray(1)

glEnable(GL_DEPTH_TEST);	
glClearColor(0.0, 0.0, 0.0, 1.0)
	
glGenBuffers(1, vboId)
glBindBuffer(GL_ARRAY_BUFFER, vboId)
glBufferData(GL_ARRAY_BUFFER, len(vboBuffer) * 4, vboBuffer, GL_STATIC_DRAW)

textureBox = image.load('box.png').get_texture()

glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, textureBox.id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

glViewport(0, 0, width, height)

TICKS_PER_SEC = 90
pyglet.clock.schedule_interval(update, 1.0 / TICKS_PER_SEC)

pyglet.app.run()
