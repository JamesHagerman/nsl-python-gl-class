
import pyglet
from pyglet.gl import *
from pyglet import image

from shader import Shader
from math3d import *

width = 800
height = 600

cubeBuffer = [
				-1.0, 1.0, -1.0,	0,1,0,		0,0,	-1.0, 1.0, 1.0,		0,1,0,		 1,0,	 1.0, 1.0, 1.0,		0,1,0,		1,1,
				-1.0, 1.0, -1.0,	0,1,0,		0,0,	 1.0, 1.0, 1.0,		0,1,0,		 1,1,	 1.0, 1.0, -1.0,	0,1,0,		0,1,

				1.0, -1.0, -1.0,	0,-1,0,		0,0,	 1.0, -1.0, 1.0,	0,-1,0,		 1,0,	-1.0, -1.0, 1.0,	0,-1,0,		1,1,
				1.0, -1.0, -1.0,	0,-1,0,		0,0,	-1.0, -1.0, 1.0,	0,-1,0,		 1,1,	-1.0, -1.0, -1,		0,-1,0,		0,1,

				-1.0, -1.0, -1,		-1,0,0,		0,0,	-1.0, -1.0, 1.0,	-1,0,0,		 1,0,	-1.0, 1.0, 1.0,		-1,0,0,		1,1,
				-1.0, -1.0, -1,		-1,0,0,		0,0,	-1.0, 1.0, 1.0,		-1,0,0,		 1,1,	-1.0, 1.0, -1.0,	-1,0,0,		0,1,

				1.0, -1.0, 1.0,		1,0,0,		0,0,	 1.0, -1.0, -1.0,	1,0,0,		 1,0,	 1.0, 1.0, -1.0,	1,0,0,		1,1,
				1.0, -1.0, 1.0,		1,0,0,		0,0,	 1.0, 1.0, -1.0,	1,0,0,		 1,1,	 1.0, 1.0, 1.0,		1,0,0,		0,1,

				1.0, 1.0, -1.0,		0,0,-1,		0,0,	 1.0, -1.0, -1.0,	0,0,-1,		 1,0,	-1.0, -1.0, -1,		0,0,-1,		1,1,
				1.0, 1.0, -1.0,		0,0,-1,		0,0,	-1.0, -1.0, -1,		0,0,-1,		 1,1,	-1.0, 1.0, -1.0,	0,0,-1,		0,1,

				-1.0, -1.0, 1.0,	0,0,1,		0,0,	 1.0, -1.0, 1.0,	0,0,1,		 1,0,	 1.0, 1.0, 1.0,		0,0,1,		1,1,
				-1.0, -1.0, 1.0,	0,0,1,		0,0,	 1.0, 1.0, 1.0,		0,0,1,		 1,1,	-1.0, 1.0, 1.0,		0,0,1,		0,1,
			]

groundBuffer = [
				-100.0, -1.0, -100.0,	0,1,0,		0,0,	-100.0, -1.0, 100.0,		0,1,0,		 100,0,	 	100.0, -1.0, 100.0,			0,1,0,		100,100,
				-100.0, -1.0, -100.0,	0,1,0,		0,0,	 100.0, -1.0, 100.0,		0,1,0,		 100,10,	 100.0, -1.0, -100.0,		0,1,0,		0,100,
			   ]

GL_ELEMENT_ARRAY_BUFFER = 34963

window = pyglet.window.Window(width=width, height=height)

vboId = GLuint()
vboGroundId = GLuint()

textureId = GLuint()

vboBuffer = (GLfloat * len(cubeBuffer))(*cubeBuffer)
vboGround = (GLfloat * len(groundBuffer))(*groundBuffer)

myShader = Shader(''.join(open('bump.v.glsl')),''.join(open('bump.f.glsl')))

myTime = 0
modelMatrix = identityMatrix
viewMatrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, -4, 1]
projMatrix = perspectiveGL(65.0, width / float(height), 0.1, 200.0)

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

	myShader.uniformi('colorMap', 0);
	myShader.uniformi('normalMap', 1);
	myShader.uniformi('aoMap', 2);
	myShader.uniformi('roMap', 3);

	glBindBuffer(GL_ARRAY_BUFFER, vboId)

	glEnableVertexAttribArray(0)
	glEnableVertexAttribArray(1)
	glEnableVertexAttribArray(2)

	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, 0)
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, 12)
	glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, 24)

	glDrawArrays(GL_TRIANGLES, 0, len(vboBuffer) / 8)

	myShader.uniformi('colorMap', 4);
	myShader.uniformi('normalMap', 5);
	myShader.uniformi('aoMap', 6);
	myShader.uniformi('roMap', 6);

	glBindBuffer(GL_ARRAY_BUFFER, vboGroundId)

	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, 0)
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, 12)
	glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, 24)

	glDrawArrays(GL_TRIANGLES, 0, len(vboGround) / 8)


glEnable(GL_DEPTH_TEST);
glClearColor(0.0, 0.0, 0.0, 1.0)

glGenBuffers(1, vboId)
glBindBuffer(GL_ARRAY_BUFFER, vboId)
glBufferData(GL_ARRAY_BUFFER, len(vboBuffer) * 4, vboBuffer, GL_STATIC_DRAW)

glGenBuffers(1, vboGroundId)
glBindBuffer(GL_ARRAY_BUFFER, vboGroundId)
glBufferData(GL_ARRAY_BUFFER, len(vboGround) * 4, vboGround, GL_STATIC_DRAW)

textureBox = 	image.load('box.png').get_texture()
textureNormal = image.load('boxNormal.png').get_texture()
textureAO = 	image.load('boxAO.png').get_texture()
textureRO = 	image.load('boxRO.png').get_texture()
ground = 		image.load('ground.png').get_texture()
groundNorm = 	image.load('groundNorm.png').get_texture()
white		 =	image.load('white.png').get_texture()

glActiveTexture(GL_TEXTURE0)
glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, textureBox.id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

glActiveTexture(GL_TEXTURE1)
glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, textureNormal.id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

glActiveTexture(GL_TEXTURE2)
glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, textureAO.id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

glActiveTexture(GL_TEXTURE3)
glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, textureRO.id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

glActiveTexture(GL_TEXTURE4)
glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, ground.id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

glActiveTexture(GL_TEXTURE5)
glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, groundNorm.id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

glActiveTexture(GL_TEXTURE6)
glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, white.id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

glViewport(0, 0, width, height)

TICKS_PER_SEC = 90
pyglet.clock.schedule_interval(update, 1.0 / TICKS_PER_SEC)

pyglet.app.run()
