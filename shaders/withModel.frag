#version 330

uniform int with_texture;
uniform int clear_sea;
uniform float sea_level;
uniform float sl_gap;
uniform float sand_level;
uniform float ssl_gap;
uniform float grass_level;
uniform float gll_gap;
uniform float rock_level;
uniform float rl_gap;

uniform sampler2D color_map;

uniform sampler2D sea;
uniform sampler2D sand;
uniform sampler2D grass;
uniform sampler2D rock;
uniform sampler2D snow;

uniform vec4 sea_color;
uniform vec4 sand_color;
uniform vec4 grass_color;
uniform vec4 rock_color;
uniform vec4 ice_color;

uniform	vec4 diffuse;
uniform	vec4 specular;
uniform	float shininess;
uniform	mat3 m_normal;

in Data {
	vec4 eye;
	vec3 normal;
	vec3 l_dir;
    vec2 texCoord;
	float height;
} DataIn;

out vec4 colorOut;

void main() {

	// set the specular term to black
	vec4 spec = vec4(0.0);

    vec4 sea_t = texture(sea, DataIn.texCoord);
	vec4 sand_t = texture(sand, DataIn.texCoord);
	vec4 grass_t = texture(grass, DataIn.texCoord);
	vec4 rock_t = texture(rock, DataIn.texCoord);
	vec4 snow_t = texture(snow, DataIn.texCoord);
    vec4 color = texture(color_map, DataIn.texCoord);

	// normalize both input vectors
	vec3 n = normalize(DataIn.normal);
	if (DataIn.height <= sea_level-sl_gap && clear_sea == 1) n = normalize(m_normal * vec3(0,1,0));
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

	float f1 = smoothstep(sea_level-sl_gap,sea_level+sl_gap,DataIn.height);
	float f2 = smoothstep(sand_level-ssl_gap,sand_level+ssl_gap,DataIn.height);
	float f3 = smoothstep(grass_level-gll_gap,grass_level+gll_gap,DataIn.height);
	float f4 = smoothstep(rock_level-rl_gap,rock_level+rl_gap,DataIn.height);

	if (with_texture==0){
		if (f1<1) color = mix(sea_color,sand_color,f1);
		else if (f2<1) color = mix(sand_color,grass_color,f2);
		else if (f3<1) color = mix(grass_color,rock_color,f3);
		else if (f4<1) color = mix(rock_color,ice_color,f4);
		else color = ice_color;
	}
	else{
		if (f1<1) color = mix(sea_t,sand_t,f1);
		else if (f2<1) color = mix(sand_t,grass_t,f2);
		else if (f3<1) color = mix(grass_t,rock_t,f3);
		else if (f4<1) color = mix(rock_t,snow_t,f4);
		else color = snow_t;
	}

	colorOut = max(intensity * color + spec, color * 0.25);

}