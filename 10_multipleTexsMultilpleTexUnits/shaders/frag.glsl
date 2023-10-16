#version 330 core

in vec3 fragColor;
in vec2 fragUV;

out vec4 outColor;

uniform sampler2D tex0;
uniform sampler2D tex1;

void main(){
    outColor = mix(texture(tex0, fragUV), texture(tex1, fragUV), 0.5);
}