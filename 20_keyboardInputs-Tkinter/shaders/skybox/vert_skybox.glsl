#version 420 core

// Attributes
layout (location = 0) in vec3 position;    // we can also use layout to specify the location of the attribute
layout (location = 1) in vec3 uv;
layout (location = 2) in vec3 normal;

out vec2 clipboxPosition;

void main(){
    clipboxPosition = position.xy;
    gl_Position = vec4(position.xy, 1.0, 1.0);
}
