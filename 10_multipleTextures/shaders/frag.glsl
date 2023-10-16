#version 330 core

in vec3 fragColor;
in vec2 fragUV;

out vec4 outColor;

uniform sampler2D tex;

void main(){
    vec3 materialColor = texture(tex, fragUV).rgb;
    outColor = vec4( materialColor, 1.0 );

    // or if you want to use the color as well :
    // outColor = vec4( materialColor * fragColor, 1.0 );
}