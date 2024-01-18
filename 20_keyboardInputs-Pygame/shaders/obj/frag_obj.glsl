#version 420 core

in vec2 fragUV;

layout (binding=0) uniform sampler2D tex2D;

out vec4 outColor;


void main(){
    vec3 texColor = texture(tex2D,fragUV).rgb;
    outColor = vec4(texColor, 1.0);
}