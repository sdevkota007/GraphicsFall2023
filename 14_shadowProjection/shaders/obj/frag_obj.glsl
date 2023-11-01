#version 420 core


in vec2 fragUV;
in vec3 fragPos, fragNormal;

layout (binding=0) uniform sampler2D tex2D;

uniform vec3 lightPos;

out vec4 outColor;

float computeDiffuseFactor()
{
    vec3 N = normalize(fragNormal);
    vec3 L = normalize(lightPos-fragPos);
    return clamp(dot(L,N), 0.,1.);
}

void main(){
    float df = computeDiffuseFactor();
    vec3 texColor = texture(tex2D,fragUV).rgb;
    outColor = vec4(texColor * df + 0.1, 1.0);
}