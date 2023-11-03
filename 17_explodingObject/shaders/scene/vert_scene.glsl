#version 420 core

// Attributes
layout (location = 0) in vec3 position;    // we can also use layout to specify the location of the attribute
layout (location = 1) in vec2 uv;
layout (location = 2) in vec3 normal;

out VS_OUT {
    vec2 uv;
} vs_out;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main(){
    gl_PointSize = 100.0;
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    vs_out.uv = uv;
}