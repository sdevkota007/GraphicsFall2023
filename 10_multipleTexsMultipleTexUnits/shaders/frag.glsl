#version 420 core

in vec3 fragColor;
in vec2 fragUV;

out vec4 outColor;

layout (binding=0) uniform sampler2D tex0;  // attach tex0 to texture unit 0
layout (binding=1) uniform sampler2D tex1;  // attach tex1 to texture unit 1

void main(){
    outColor = mix(texture(tex0, fragUV), texture(tex1, fragUV), 0.5);
}