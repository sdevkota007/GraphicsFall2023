#version 420 core

// Attributes
layout (location = 0) in vec3 position;    // we can also use layout to specify the location of the attribute
layout (location = 1) in vec2 uv;
layout (location = 2) in vec3 normal;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec3 fragNormal;
out vec3 fragPos;

void main(){
    gl_Position =  projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);

    // Transform the normal from object (or model) space to world space
    fragPos = (modelMatrix * vec4(position, 1.0)).xyz;
    fragNormal = (transpose(inverse(modelMatrix))*vec4(normal,0)).xyz;
}