#version 330 core

in vec3 fragNormal;
out vec4 outColor;

void main(){
    vec3 N = abs(normalize(fragNormal));
    outColor = vec4(N, 1.0);
    // OR
    //outColor = vec4( 0.5f * ( fragNormal + 1.0f ), 1.0f );
}