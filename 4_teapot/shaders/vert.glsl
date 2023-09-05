#version 330 core

in vec3 position; // Attribute
in vec3 normal; // Attribute

out vec3 fragColor;

uniform float scale;
uniform float center;

void main(){
    vec3 pos = position-center;
    gl_Position = vec4(pos * scale, 1.0);
    fragColor = normalize(normal);
}
