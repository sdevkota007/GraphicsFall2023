#version 330 core

in vec2 fragUV;
uniform sampler2D tex2D;

out vec4 outColor;

void main(){
    vec3 texColor = texture(tex2D, fragUV).rgb;
    outColor = vec4(texColor, 1.0);
}