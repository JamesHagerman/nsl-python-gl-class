#version 300 es

#ifdef GL_ES
precision mediump float;
#endif

uniform sampler2D colorMap;

out vec4 outputColor;

smooth in vec2 uv;

void main()
{
	vec4 color = texture2D(colorMap, uv);

	outputColor = color;
}
