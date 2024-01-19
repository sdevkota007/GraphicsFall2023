#version 330 core

// Attributes
layout (location = 0) in vec2 position;    // we can also use layout to specify the location of the attribute

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main () {
  gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 0, 1);
}





