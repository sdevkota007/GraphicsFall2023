#version 420 core

// Attributes
layout (location = 0) in vec3 position;    // we can also use layout to specify the location of the attribute
layout (location = 1) in vec2 uv;
layout (location = 2) in vec3 normal;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

// for shadow computation
uniform vec3 planeNormal;
uniform vec3 lightPos;
uniform vec3 pointOnPlane;
uniform bool shadowFlag;

void main(){
    // Transform the position from object (or model) space to clip space. Range [-1,1] in all 3 dimensions
    vec4 worldPos =  modelMatrix * vec4(position, 1.0);
    vec3 pos = worldPos.xyz;

    // get positions of shadow projection in world space
    vec3 q = pointOnPlane + 0.001*planeNormal;
    float t =  dot((q- pos), planeNormal) / dot((pos - lightPos) , planeNormal);
    vec3 shadowPos = pos + t * (pos - lightPos);

    gl_Position = projectionMatrix * viewMatrix*vec4(shadowPos,1);
}