#version 330

uniform sampler2D tex;
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
    vec4 color = texture(tex, DataIn.texCoord);
	vec4 spec = vec4(0.0);
    float height = color.r;

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
	colorOut = color;
}