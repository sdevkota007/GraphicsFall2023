#version 330 core

in vec3 fragColor;
out vec4 outColor;

void main(){
    vec3 N = abs(normalize(fragColor));
    outColor = vec4(N, 1.0);
}