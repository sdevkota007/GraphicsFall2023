#version 420 core

in vec3 fragColor;
in vec2 fragUV;

out vec4 outColor;

layout (binding=0) uniform sampler2D tex;   // attach tex to texture unit 0

void main(){
    vec3 materialColor = texture(tex, fragUV).rgb;
     outColor = vec4( materialColor, 1.0 );
    // or if you want to use the color as well :
    // outColor = vec4( materialColor * fragColor, 1.0 );
}