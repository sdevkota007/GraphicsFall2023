#version 420 core

layout (triangles) in;
layout (triangle_strip, max_vertices = 5) out;

in vec3 geomNormal[];
out vec3 fragNormal;

uniform bool addFourthVertex;

void main() {
    gl_Position = gl_in[0].gl_Position;
    fragNormal = geomNormal[0];         // Normal
    EmitVertex();

    gl_Position = gl_in[1].gl_Position;
    fragNormal = vec3(1, 0, 0);         // R
    EmitVertex();

    gl_Position = gl_in[2].gl_Position/2.0;
    fragNormal = vec3(0, 1, 0);         // G
    EmitVertex();

    if (addFourthVertex) {
        gl_Position = vec4(1.0, 0.0, 0.0, 1.0);    // picking a random position for the 4th vertex
        fragNormal = vec3(0, 0, 1);         // B
        EmitVertex();
    }


    EndPrimitive();
}
