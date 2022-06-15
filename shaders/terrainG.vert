#version 330

uniform sampler2D height_map;
uniform sampler2D color_map;

uniform	mat4 m_pvm;
uniform	mat4 m_viewModel;
uniform	mat4 m_view;
uniform	mat3 m_normal;
uniform	vec4 l_dir;	   // global space

in vec4 position;	// local space
in vec3 normal;		// local space
in vec2 texCoord0;

// the data to be sent to the fragment shader
out Data {
	vec4 eye;
	vec3 normal;
	vec3 l_dir;
    vec2 texCoord;
} DataOut;

void main () {

	float height = texture(height_map, texCoord0).r;

	DataOut.normal = normalize(m_normal * normal);
	DataOut.eye = -(m_viewModel * position);
	DataOut.l_dir = normalize(vec3(m_view * -l_dir));
    DataOut.texCoord = texCoord0;



	gl_Position = m_pvm * normalize ((position + vec4(0,height,0,1)) * vec4(20,8,20,1));	
}
