#version 330

uniform int with_texture;
uniform float sea_level;
uniform float sl_gap;
uniform float grass_level;
uniform float gll_gap;
uniform float rock_level;
uniform float rl_gap;

uniform sampler2D height_map;
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
	float smoothHeight;
} DataIn;

out vec4 colorOut;

void main() {
	//get textures
	vec4 sea_t = texture(sea, DataIn.texCoord);
	vec4 grass_t = texture(grass, DataIn.texCoord);
	vec4 rock_t = texture(rock, DataIn.texCoord);
	vec4 snow_t = texture(snow, DataIn.texCoord);

	// set the specular term to black
    vec4 color = texture(color_map, DataIn.texCoord);
	vec4 spec = vec4(0.0);
    float height_c = texture(height_map, DataIn.texCoord).r;
	float height = smoothstep(0.8,0.9,height_c);

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
	float f1 = smoothstep(sea_level-sl_gap,sea_level+sl_gap,DataIn.smoothHeight);
	float f2 = smoothstep(grass_level-gll_gap,grass_level+gll_gap,DataIn.smoothHeight);
	float f3 = smoothstep(rock_level-rl_gap,rock_level+rl_gap,DataIn.smoothHeight);

	if (with_texture==0){
		if (f1==0) color = vec4(0,0.20,0.525,1);
		else if (f1<1) color = mix(vec4(0,0.20,0.525,1),vec4(0.3,0.76,0.15,1),f1);
		else if (f2<1) color = mix(vec4(0.3,0.76,0.15,1),vec4(0.65,0.35,0.125,1),f2);
		else if (f3<1) color = mix(vec4(0.65,0.35,0.125,1),vec4(0.98,0.98,0.98,1),f3);
		else color = vec4(0.98,0.98,0.98,1);
	}
	else{
		if (f1==0) color = sea_t;
		else if (f1<1) color = mix(sea_t,grass_t,f1);
		else if (f2<1) color = mix(grass_t,rock_t,f2);
		else if (f3<1) color = mix(rock_t,snow_t,f3);
		else color = snow_t;
	}
	/*if (height >= 0) color = vec4(0,0.20,0.525,1);
	if (height > 0.2) color = vec4(0.3,0.76,0.15,1);
	if (height > 0.55) color = vec4(0.65,0.35,0.125,1);
	if (height > 0.85) color = vec4(0.98,0.98,0.98,1);*/
	//if (height >= 0.5) color = vec4(0,0,1,1);
	//else color = vec4(0,1,0,1);
	colorOut = color;
}