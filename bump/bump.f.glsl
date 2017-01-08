#version 300 es

#ifdef GL_ES
precision mediump float;
#endif

uniform sampler2D colorMap;
uniform sampler2D normalMap;
uniform sampler2D aoMap;
uniform sampler2D roMap;

out vec4 outputColor;

smooth in vec4 eye;
smooth in vec4 worldPos;
smooth in vec3 norm;
smooth in vec2 uv;

mat3 cotangent_frame( vec3 N, vec3 p, vec2 uv )
{
    vec3 dp1 = dFdx(p);
    vec3 dp2 = dFdy(p);
    vec2 duv1 = dFdx(uv);
    vec2 duv2 = dFdy(uv);

    vec3 dp2perp = cross(dp2, N);
    vec3 dp1perp = cross(N, dp1);
    vec3 T = dp2perp * duv1.x + dp1perp * duv2.x;
    vec3 B = dp2perp * duv1.y + dp1perp * duv2.y;

    float invmax = inversesqrt(max(dot(T,T), dot(B,B)));
    return mat3(T * invmax, B * invmax, N);
}

mat3 getTBN( vec3 N, vec3 V, vec2 texcoord )								//Magic that generates a tangent matrix from thin air
{
    vec3 map = texture2D( normalMap, texcoord ).xyz;
    map = map * 255./127. - 128./127.;
    mat3 TBN = cotangent_frame( N, -V, texcoord );
    return TBN ;
}

void main()
{
	vec4 color 			= texture2D(colorMap, uv);							//Diffuse map (the material color)
	vec3 normColor 		= texture2D(normalMap, uv).rgb * 2.0 - 1.0;			//Normal map (for bump effect)
	vec3 reflectColor 	= texture2D(roMap, uv).rgb;							//Reflection occlusion map (controls specular highlights)
	vec3 ambientColor 	= texture2D(aoMap, uv).rgb;							//Ambient occlusion map (simulates self-shadowing)

	vec3 N = normalize(norm);												//Surface normal in world space
	vec3 L = normalize(vec3(4.0f, 4.0f, 4.0f) - worldPos.xyz);				//Surface-to-light in world space
	vec3 E = normalize(eye.xyz);											//Surface-to-eye in world space

	mat3 tbnMatrix = getTBN(N, E, uv);										//Transforms tangent space to world space

	N = normalize(tbnMatrix * normColor);									//Bumpy normals in worldspace

	float diffuse = max(dot(N, L), 0.0f);									//How close is the surface normal pointing at the light?
	float specular = 0.0f;

	#define attenConstant 0.01												//Light attenuation constants
	#define attenLinear 0.01
	#define attenQuad 0.03

	float D = length(vec3(4.0f, 4.0f, 4.0f) - worldPos.xyz);				//Distance from surface-to-light

	if (diffuse > 0.0)
	{
        diffuse /= (attenConstant + attenLinear * D + attenQuad * D * D);

		vec3 H = normalize(L - E);
        float NdotHV = max(dot(N, H), 0.0);
        specular = diffuse * pow(NdotHV, 30.0f);								//Specular: How much is the light reflecting toward the eye?
	}

	float ambientOcclusion = ambientColor.r;								//These maps are actually greyscale
	float reflectOcclusion = reflectColor.r;

	vec4 colorWhite = vec4(1,1,1,1);

	outputColor  = color * diffuse * ambientOcclusion		*	1.0f;		// Diffuse component (plus AO because it looks better)
	outputColor += color * ambientOcclusion					*	0.08f;		// Ambient component
	outputColor += colorWhite * specular * reflectOcclusion * 	0.6f;		// Specular component
}
