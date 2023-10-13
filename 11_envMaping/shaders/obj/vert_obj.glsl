#version 330 core

// Attributes
layout (location = 0) in vec3 position;    // we can also use layout to specify the location of the attribute
layout (location = 1) in vec2 uv;
layout (location = 1) in vec3 normal;


out vec3 fragNormal;
out vec3 fragPos;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main(){
    // Transform the position from object (or model) space to clip space. Range [-1,1] in all 3 dimensions
    vec4 pos =  modelMatrix * vec4(position, 1.0);
    vec3 fragPos = pos.xyz;
    gl_Position = projectionMatrix * viewMatrix * pos;

    // Transform the normal from object (or model) space to world space
    mat4 normal_matrix = transpose(inverse(modelMatrix));
    vec3 new_normal = (normal_matrix*vec4(normal,0)).xyz;
    fragNormal = normalize(new_normal);
}