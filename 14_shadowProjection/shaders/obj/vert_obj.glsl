#version 420 core

// Attributes
layout (location = 0) in vec3 position;    // we can also use layout to specify the location of the attribute
layout (location = 1) in vec2 uv;
layout (location = 2) in vec3 normal;


out vec2 fragUV;
out vec3 fragPos;
out vec3 fragNormal;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main(){
    // Transform the position from object (or model) space to clip space. Range [-1,1] in all 3 dimensions
    vec4 worldPos =  modelMatrix * vec4(position, 1.0);

    fragUV = uv;
    fragPos = worldPos.xyz;
    fragNormal = normalize((transpose(inverse(modelMatrix))*vec4(normal,0)).xyz);

    gl_Position = projectionMatrix * viewMatrix * worldPos;
}