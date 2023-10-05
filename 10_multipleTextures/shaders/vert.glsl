#version 330 core

in vec3 position; // Attribute
in vec2 uv; // Attribute
in vec3 color; // Attribute



out vec3 fragColor;
out vec2 fragUV;

void main(){
    gl_Position = vec4(position, 1.0);
    fragUV = uv;
    fragColor = color;

}