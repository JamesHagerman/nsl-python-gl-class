#version 330

uniform sampler2D colorMap;

out vec4 outputColor;

smooth in vec3 norm;
smooth in vec2 uv;

void main()
{
	vec4 color = texture2D(colorMap, uv);

	vec4 normColor = vec4(norm * 0.5 + 0.5, 1.0f);
	
	outputColor = normColor;
}