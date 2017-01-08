#version 330

uniform sampler2D colorMap;

out vec4 outputColor;

smooth in vec2 uv;

void main()
{
	vec4 color = texture2D(colorMap, uv);

	outputColor = color;
}