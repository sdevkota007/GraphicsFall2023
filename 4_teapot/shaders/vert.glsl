#version 330 core

layout (location = 0) in vec3 position;    // we will use layout to specify the location of the attribute 'position'
layout (location = 1) in vec3 normal;        // Attribute 'normal'

out vec3 fragColor;

uniform float scale;
uniform vec3 center;

void main(){
    vec3 pos = position-center;
    gl_Position = vec4(pos * scale, 1.0);
    fragColor = normalize(normal);
}