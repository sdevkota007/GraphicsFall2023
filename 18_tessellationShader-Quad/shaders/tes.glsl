#version 420 core

layout (quads, equal_spacing, ccw) in;

out vec3 fragColor;


vec4 interpolate(vec4 p0, vec4 p1, vec4 p2, vec4 p3) {
    float u = gl_TessCoord.x;
    float v = gl_TessCoord.y;

    vec4 p = (1.0 - u) * (1.0 - v)  * p0
           + (1.0 - v) * u          * p1
           + v * (1.0 - u)          * p3
           + u * v                  * p2;

    return p;
}

vec4 interpolate(vec4 a, vec4 b, vec4 c) {
    vec4 ab = mix(a, b, gl_TessCoord.x);
    vec4 ac = mix(c, a, gl_TessCoord.x);
    return mix(ab, ac, gl_TessCoord.y);
}

vec4 interpolate3D(vec4 v0, vec4 v1, vec4 v2)
{
    return vec4(gl_TessCoord.x) * v0 + vec4(gl_TessCoord.y) * v1 + vec4(gl_TessCoord.z) * v2;
}

void main() {
    gl_Position = interpolate(gl_in[0].gl_Position,
                              gl_in[1].gl_Position,
                              gl_in[2].gl_Position,
                              gl_in[3].gl_Position);


    fragColor = vec3(gl_TessCoord.x, gl_TessCoord.y, gl_TessCoord.z);

}
