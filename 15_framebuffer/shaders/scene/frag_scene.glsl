#version 420 core

in vec3 fragNormal;
in vec3 fragPos;

out vec4 outColor;

uniform vec3 materialColor;
uniform vec3 lightPos;

vec3 computeDiffuse(vec3 N, vec3 L){
    return materialColor * clamp(dot(N, L), 0.0, 1.0);
}

void main(){
    vec3 N = normalize(fragNormal);
    vec3 L = normalize(lightPos - fragPos);
    vec3 diffuse = computeDiffuse(N, L);

    outColor = vec4(diffuse, 1.0);
    // this can stay empty because are not shading any fragments,
    // we just want the depth of the fragments in the depth buffer
    // we don't even need the outColor statement above
}