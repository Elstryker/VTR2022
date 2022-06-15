#version 330

uniform sampler2D height_map;
uniform sampler2D color_map;

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
    vec4 color = texture(color_map, DataIn.texCoord);
	vec4 spec = vec4(0.0);
    float height = texture(height_map, DataIn.texCoord).r;

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
	float f1 = smoothstep(0.19,0.21,height);
	float f2 = smoothstep(0.54,0.56,height);
	float f3 = smoothstep(0.84,0.86,height);
	if (f1==0) color = vec4(0,0.20,0.525,1);
	else if (f1<1) color = mix(vec4(0,0.20,0.525,1),vec4(0.3,0.76,0.15,1),f1);
	else if (f2<1) color = mix(vec4(0.3,0.76,0.15,1),vec4(0.65,0.35,0.125,1),f2);
	else if (f3<1) color = mix(vec4(0.65,0.35,0.125,1),vec4(0.98,0.98,0.98,1),f3);
	else color = vec4(0.98,0.98,0.98,1);
	/*if (height >= 0) color = vec4(0,0.20,0.525,1);
	if (height > 0.2) color = vec4(0.3,0.76,0.15,1);
	if (height > 0.55) color = vec4(0.65,0.35,0.125,1);
	if (height > 0.85) color = vec4(0.98,0.98,0.98,1);*/
	//if (height >= 0.5) color = vec4(0,0,1,1);
	//else color = vec4(0,1,0,1);
	colorOut = color;
}