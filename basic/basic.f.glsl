#version 300 es

#ifdef GL_ES
precision mediump float;
#endif

out vec4 outputColor;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projMatrix;

void main()
{
	 outputColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
}
