#version 330

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projMatrix;

smooth out vec4 worldPos;
smooth out vec3 norm;
smooth out vec2 uv;

void main()
{
	mat3 normalMatrix = mat3(transpose(inverse(modelMatrix)));
	mat4 pmvMatrix = projMatrix * viewMatrix * modelMatrix;
	
	gl_Position = pmvMatrix * vec4(position, 1.0f);
	
	worldPos = modelMatrix * vec4(position, 1.0f);
	norm = normalize(normalMatrix * normal);
	
	uv = texCoords;
}