#version 420 core

in vec2 fragUV;

out vec4 outColor;

layout (binding=0) uniform sampler2D tex;

void main(){
    vec3 texColor = texture(tex, fragUV).rgb;
    outColor = vec4(texColor, 1.0);
}