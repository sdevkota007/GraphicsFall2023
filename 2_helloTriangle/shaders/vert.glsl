#version 330 core

layout (location = 0) in vec3 position;    // we will use layout to specify the location of the attribute 'position'
layout (location = 1) in vec3 color;        // Attribute 'color'

out vec3 fragColor;

void main(){
    gl_Position = vec4(position, 1.0);
    fragColor = color;
}