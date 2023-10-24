#version 420 core

in vec2 clipboxPosition;
out vec4 outColor;

uniform float near;
uniform float far;

layout (binding=0) uniform sampler2D depthTex;

float linearize_depth(float depth, float near, float far){
    float z = depth * 2.0 - 1.0; // [0, 1] -> [-1, 1]
    return (2.0 * near * far) / (far + near - z * (far - near));
}


void main(){
    vec2 uv = clipboxPosition * 0.5 + 0.5;
    float depth = texture(depthTex, uv).r;

    // We know due to perspective projection, the depth is non-linear,
    // so let's linearize the depth value and change the range from [0, far] to [0, 1] for visualization
    depth = linearize_depth(depth, near, far);
    depth = depth / far;

    outColor = vec4(vec3(depth), 1.0);
}

// reference: https://learnopengl.com/Advanced-OpenGL/Depth-testing
