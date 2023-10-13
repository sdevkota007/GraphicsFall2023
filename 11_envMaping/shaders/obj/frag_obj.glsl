#version 330 core

in vec3 fragNormal;
in vec3 fragPos;

uniform vec3 eyePos;
uniform samplerCube cubeMapTex;

out vec4 outColor;

void main(){
    vec3 N = normalize(fragNormal);
    vec3 V = normalize(eyePos - fragPos);
    vec3 R = reflect(-V, N);
    vec3 envColor = texture(cubeMapTex, R).rgb;

    outColor = vec4(envColor, 1.0);
}


//void main(){
//    vec3 N = normalize(fragNormal);
//    outColor = vec4(abs(N), 1.0);
//}