
import pyglet
from pyglet.gl import *
from pyglet import image

from shader import *
from math3d import *


# Each line here is a triangle:
cubeBuffer = [
# top face:
				-1.0, 1.0, -1.0,	-1.0, 1.0, 1.0,		1.0, 1.0, 1.0,
				-1.0, 1.0, -1.0,	 1.0, 1.0, 1.0,		1.0, 1.0, -1.0,

				1.0, -1.0, -1.0,	 1.0, -1.0, 1.0,	-1.0, -1.0, 1.0,
				1.0, -1.0, -1.0,	-1.0, -1.0, 1.0,	-1.0, -1.0, -1,

				-1.0, -1.0, -1,		-1.0, -1.0, 1.0,	-1.0, 1.0, 1.0,
				-1.0, -1.0, -1,		-1.0, 1.0, 1.0,		-1.0, 1.0, -1.0,

				1.0, -1.0, 1.0,		 1.0, -1.0, -1.0,	 1.0, 1.0, -1.0,
				1.0, -1.0, 1.0,		 1.0, 1.0, -1.0,	 1.0, 1.0, 1.0,

				1.0, 1.0, -1.0,		 1.0, -1.0, -1.0,	-1.0, -1.0, -1,
				1.0, 1.0, -1.0,		-1.0, -1.0, -1,		-1.0, 1.0, -1.0,

				-1.0, -1.0, 1.0,	 1.0, -1.0, 1.0,	 1.0, 1.0, 1.0,
				-1.0, -1.0, 1.0,	 1.0, 1.0, 1.0,		-1.0, 1.0, 1.0,
			]


GL_ELEMENT_ARRAY_BUFFER = 34963

width = 800
height = 600

window = pyglet.window.Window(width=width, height=height) # , fullscreen=True (escape to exit!)

vboId = GLuint()

# This turns the above array into an array of C-types:
vboBuffer = (GLfloat * len(cubeBuffer))(*cubeBuffer)

# This will load in the vertex and fragment shader:
myShader = Shader(''.join(open('basic.v.glsl')),''.join(open('basic.f.glsl')))

# This is global time... because we should keep track of ticks...
myTime = 0

# OpenGL expects types as column first matrices (for homogeneous tranforms):
# This starts the model's matrix as the equivilant of "one" in integer math:
modelMatrix = identityMatrix

# This moves the points INTO the screen:
viewMatrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, -4, 1]

# This sets up the perspective camera's projection matricies:
projMatrix = perspectiveGL(65.0, width / float(height), 1.0, 20.0)

def update(dt):
	# Our update method:
	global myTime, modelMatrix # global will make these variables persist
	modelMatrix = rotMatrixY(myTime)
	myTime += 1 # Add a tick for ever frame!

@window.event
def on_draw():
	# Gets called every frame

	# Clear the depth buffer and the color buffer. This will clear the screen:
	glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)

	# This binds our awesome shader
	myShader.bind()

	# These just define "some variables" that we can use in the shader
	myShader.uniform_matrixf('modelMatrix', modelMatrix)
	myShader.uniform_matrixf('viewMatrix', viewMatrix)
	myShader.uniform_matrixf('projMatrix', projMatrix)

	# Makes the vboId buffer work in the shader
	glBindBuffer(GL_ARRAY_BUFFER, vboId)

	# This defines WHERE the data is located in the vboId buffer... NOT how it
	# is structured:
	glEnableVertexAttribArray(0)

	# This tells the GPU HOW that VBO buffer is organized:
	# 0 is WHICH attribute we're actually digging through
	# 3 is how many items
	# gl_float is the type of the item
	# gl_false is just a setting to
	# 3 * 4 is "how far to jump into the array" to get to the next item
	# 0 is the offset
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, 0)

	# This tells the GPU to draw some type using data from an array:
	# GL_TRIANGLES means we're drawing tri's from the vbo
	# 0 is offset??
	# last is "3 elements per point"
	glDrawArrays(GL_TRIANGLES, 0, len(vboBuffer) / 3)

	glDisableVertexAttribArray(0)


# Configure OpenGL because it needs some help

# This keeps track of the last depth drawn at this pixel:
glEnable(GL_DEPTH_TEST);

# Clear color for the "no object drawn" pixels (fragments)
glClearColor(0.0, 0.0, 0.0, 1.0)

# Building a reference to the vboId buffer in the GPU:
glGenBuffers(1, vboId)
# Bind that buffer as an array buffer in the GPU
# All functions will act on THIS buffer:
glBindBuffer(GL_ARRAY_BUFFER, vboId)
# Shove some data at that buffer (in this case, it's the cube's vertecies)
# 4 bytes per float is why we do *4... so it's saying how many bytes we need:
# GL_STATIC_DRAW is because we probably don't need to change that geometry
# "bandwidth": is the process of hucking this data at the GPU:
glBufferData(GL_ARRAY_BUFFER, len(vboBuffer) * 4, vboBuffer, GL_STATIC_DRAW)

# This defines the viewport we'll be drawing into... Doesn't seem to be needed
# pyglet problably does this...
# glViewport(0, 0, width, height)

# Sets up the pyglet render speed:
TICKS_PER_SEC = 90
pyglet.clock.schedule_interval(update, 1.0 / TICKS_PER_SEC)

# Start pyglet off on running it's on_draw() stuff
pyglet.app.run()
