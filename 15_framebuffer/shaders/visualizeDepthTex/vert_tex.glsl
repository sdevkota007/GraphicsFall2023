#version 420 core

// Attributes
layout (location = 0) in vec3 position;    // we can also use layout to specify the location of the attribute

out vec2 clipboxPosition;

void main(){
    clipboxPosition = position.xy;
    gl_Position = vec4(position, 1.0);
}
