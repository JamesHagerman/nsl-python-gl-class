#version 300 es

layout(location = 0) in vec3 position;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projMatrix;

// You can also hand some data through the pipe that skips the rasterizer..
// We'll do that later...

void main()
{
	mat4 pmvMatrix = projMatrix * viewMatrix * modelMatrix;

	gl_Position = pmvMatrix * vec4(position, 1.0f);

}
