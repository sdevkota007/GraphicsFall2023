#version 330 core

in vec3 position; // Attribute
in vec3 color; // Attribute

out vec3 fragColor;

void main(){
    gl_Position = vec4(position, 1.0);
    fragColor = color;
}