#version 330 core

in vec3 position; // Attribute
in vec3 normal;   // Attribute

uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

out vec3 fragNormal;

void main(){
    // Transform the position from object (or model) space to clip space. Range [-1,1] in all 3 dimensions
    vec4 pos = projection_matrix * view_matrix * model_matrix * vec4(position, 1.0);
    gl_Position = pos;

    // Transform the normal from object (or model) space to world space
    mat4 normal_matrix = transpose(inverse(model_matrix));
    vec3 new_normal = (normal_matrix*vec4(normal,0)).xyz;
    fragNormal = normalize(new_normal);
//    fragNormal = normalize(normal);
}