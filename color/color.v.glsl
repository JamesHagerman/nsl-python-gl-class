#version 300 es

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projMatrix;

// This hands this value through to the fragment shader (skips the rasterer!)
smooth out vec4 col;

void main()
{
	mat4 pmvMatrix = projMatrix * viewMatrix * modelMatrix;

	gl_Position = pmvMatrix * vec4(position, 1.0f);

	col = vec4(color, 1.0f);

}
