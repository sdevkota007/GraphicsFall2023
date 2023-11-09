#version 420 core

layout (triangles, equal_spacing, ccw) in;


vec4 interpolate3D(vec4 v0, vec4 v1, vec4 v2)
{
    return vec4(gl_TessCoord.x) * v0 + vec4(gl_TessCoord.y) * v1 + vec4(gl_TessCoord.z) * v2;
}

void main() {

    gl_Position = interpolate3D(gl_in[0].gl_Position,
                              gl_in[1].gl_Position,
                              gl_in[2].gl_Position);

}
