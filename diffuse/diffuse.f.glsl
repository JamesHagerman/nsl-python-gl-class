#version 330

uniform sampler2D colorMap;

out vec4 outputColor;

smooth in vec4 worldPos;
smooth in vec3 norm;
smooth in vec2 uv;

void main()
{
	vec4 color = texture2D(colorMap, uv);
		
	vec3 L = normalize(worldPos.xyz - vec3(4.0f, 4.0f, -4.0f));
	vec3 N = norm;
	
	float diffuse = max(dot(N, L), 0.0f);
	
	outputColor = color * diffuse;
}