#version 420 core

layout(binding=0)uniform samplerCube cubeMapTex;
uniform mat4 invViewProjectionMatrix;

in vec2 clipboxPosition;
out vec4 outColor;

void main(){
    vec4 direction_4d = invViewProjectionMatrix * vec4(clipboxPosition, 1, 1);
    vec3 direction_3d = normalize(direction_4d.xyz / direction_4d.w);
    outColor = texture(cubeMapTex, direction_3d);

}
