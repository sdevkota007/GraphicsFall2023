#version 330 core

in vec3 position; // Attribute
in vec3 normal;   // Attribute

out vec3 fragNormal;

void main(){
    gl_Position = vec4(position, 1.0);
    fragNormal = normalize(normal);
}