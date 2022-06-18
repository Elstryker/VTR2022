#version 330

uniform int with_texture;

uniform sampler2D color_map;

uniform sampler2D sea;
uniform sampler2D grass;
uniform sampler2D rock;
uniform sampler2D snow;

uniform	vec4 diffuse;
uniform	vec4 specular;
uniform	float shininess;

in Data {
	vec4 eye;
	vec3 normal;
	vec3 l_dir;
    vec2 texCoord;
} DataIn;

out vec4 colorOut;

void main() {

	// set the specular term to black
	vec4 spec = vec4(0.0);

    vec4 sea_t = texture(sea, DataIn.texCoord);
	vec4 grass_t = texture(grass, DataIn.texCoord);
	vec4 rock_t = texture(rock, DataIn.texCoord);
	vec4 snow_t = texture(snow, DataIn.texCoord);
    vec4 color = texture(color_map, DataIn.texCoord);

	// normalize both input vectors
	vec3 n = normalize(DataIn.normal);
	vec3 e = normalize(vec3(DataIn.eye));
	vec3 l = DataIn.l_dir;
	
	float intensity = max(dot(n,l), 0.0);

	// if the vertex is lit compute the specular color
	if (intensity > 0.0) {
		// compute the half vector
		vec3 h = normalize(l + e);	
		// compute the specular intensity
		float intSpec = max(dot(h,n), 0.0);
		// compute the specular term into spec
		spec = specular * pow(intSpec,shininess);
	}

    vec4 finalColor = color;

    // if(with_texture == 0) {
    //     finalColor = color/255.0;
    // }
    // else {
    //     finalColor = vec4(0.5);
    // }

	colorOut = max(intensity * finalColor + spec, finalColor * 0.25);
    // colorOut = finalColor;
}