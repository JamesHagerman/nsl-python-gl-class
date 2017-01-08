#version 330

out vec4 outputColor;

smooth in vec4 col;

void main()
{
	outputColor = col;
}