#version 300 es

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projMatrix;

smooth out vec3 norm;
smooth out vec2 uv;

void main()
{
	// This allows us to keep the normals pointing in the right direction as the
	// model is rotated... AND keeps them normalized!
	mat3 normalMatrix = mat3(transpose(inverse(modelMatrix)));
	mat4 pmvMatrix = projMatrix * viewMatrix * modelMatrix;

	gl_Position = pmvMatrix * vec4(position, 1.0f);
	norm = normalMatrix * normal;

	uv = texCoords;
}
