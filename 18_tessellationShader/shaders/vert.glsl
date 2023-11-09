#version 420 core

// Attributes
layout (location = 0) in vec3 position;    // we can also use layout to specify the location of the attribute
layout (location = 1) in vec2 uv;
layout (location = 2) in vec3 normal;

uniform mat4 modelMatrix;


void main(){
    gl_Position = modelMatrix * vec4(position, 1.0);
}