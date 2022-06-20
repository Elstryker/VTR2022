#version 330

uniform int with_texture;
uniform float sea_level;
uniform float sl_gap;
uniform float sand_level;
uniform float ssl_gap;
uniform float grass_level;
uniform float gll_gap;
uniform float rock_level;
uniform float rl_gap;

uniform sampler2D height_map;
uniform sampler2D color_map;
uniform sampler2D normal_map;

uniform sampler2D sea;
uniform sampler2D sand;
uniform sampler2D grass;
uniform sampler2D rock;
uniform sampler2D snow;

uniform	vec4 diffuse;
uniform	vec4 specular;
uniform	float shininess;
uniform	mat3 m_normal;

in Data {
	vec4 eye;
	vec3 normal;
	vec3 l_dir;
    vec2 texCoord;
	float smoothHeight;
	vec4 position;
} DataIn;

out vec4 colorOut;

void main() {
	vec3 n_t = vec3(texture(normal_map,DataIn.texCoord))*2-(1,1,1);
	vec3 normall = normalize(m_normal*n_t);
	//normall = normalize(m_normal * vec3(0,1,0));
	vec3 xdiv = vec3(dFdx(DataIn.position));
	vec3 ydiv = vec3(dFdy(DataIn.position));
	//vec3 normall = normalize(m_normal * cross(xdiv, ydiv));
	if (DataIn.smoothHeight <= sea_level-sl_gap) normall = normalize(m_normal * vec3(0,1,0));

	//get textures
	vec4 sea_t = texture(sea, DataIn.texCoord);
	vec4 sand_t = texture(sand, DataIn.texCoord);
	vec4 grass_t = texture(grass, DataIn.texCoord);
	vec4 rock_t = texture(rock, DataIn.texCoord);
	vec4 snow_t = texture(snow, DataIn.texCoord);

	// set the specular term to black
    vec4 color = texture(color_map, DataIn.texCoord);
	vec4 spec = vec4(0.0);
    float height_c = texture(height_map, DataIn.texCoord).r;
	float height = smoothstep(0.8,0.9,height_c);

	// normalize both input vectors
	vec3 n = normall;
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
	float f2 = smoothstep(sand_level-ssl_gap,sand_level+ssl_gap,DataIn.smoothHeight);
	float f3 = smoothstep(grass_level-gll_gap,grass_level+gll_gap,DataIn.smoothHeight);
	float f4 = smoothstep(rock_level-rl_gap,rock_level+rl_gap,DataIn.smoothHeight);

	if (with_texture==0){
		if (f1<1) color = mix(vec4(0,0.20,0.525,1),vec4(0.83,0.78,0.46,1),f1);
		else if (f2<1) color = mix(vec4(0.83,0.78,0.46,1),vec4(0.3,0.76,0.15,1),f2);
		else if (f3<1) color = mix(vec4(0.3,0.76,0.15,1),vec4(0.65,0.35,0.125,1),f3);
		else if (f4<1) color = mix(vec4(0.65,0.35,0.125,1),vec4(0.98,0.98,0.98,1),f4);
		else color = vec4(0.98,0.98,0.98,1);
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