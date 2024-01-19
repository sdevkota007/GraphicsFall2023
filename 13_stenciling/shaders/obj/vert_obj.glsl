#version 330 core

// Attributes
layout (location = 0) in vec3 position;    // we can also use layout to specify the location of the attribute
layout (location = 1) in vec2 uv;
layout (location = 2) in vec3 normal;


out vec2 fragUV;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main(){
    // Transform the position from object (or model) space to clip space. Range [-1,1] in all 3 dimensions
    vec4 pos =  modelMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * viewMatrix * pos;

    // Send UV to fragment shader
    fragUV = uv;
}