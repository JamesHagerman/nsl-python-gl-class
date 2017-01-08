#version 300 es

#ifdef GL_ES
precision mediump float;
#endif

out vec4 outputColor;

smooth in vec4 col;

void main()
{
	outputColor = col;
}
