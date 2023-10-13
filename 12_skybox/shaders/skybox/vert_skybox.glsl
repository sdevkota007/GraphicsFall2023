#version 330 core

// Attributes
layout (location = 0) in vec2 position;    // we can also use layout to specify the location of the attribute

out vec2 clipboxPosition;

void main(){
    clipboxPosition = position;
    gl_Position = vec4(position, 1.0, 1.0);
}
