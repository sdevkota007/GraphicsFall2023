#version 420 core

layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

in VS_OUT {
    vec2 uv;
} gs_in[];

out vec2 fragUV;

uniform float time;
uniform float velocity;
uniform float acceleration;

uniform bool isSanding;

vec4 explode(vec4 position, vec3 normal)
{
    // displacement = vt + (1/2)at^2
    float displacement = velocity * time + 0.5 * acceleration * time * time;
    return position + vec4(normal, 0.0) * displacement;
}

vec3 GetNormal()
{
    vec3 a = vec3(gl_in[0].gl_Position) - vec3(gl_in[1].gl_Position);
    vec3 b = vec3(gl_in[2].gl_Position) - vec3(gl_in[1].gl_Position);
    return normalize(cross(a, b));
}

void main() {
    vec3 normal = GetNormal();

    gl_Position = explode(gl_in[0].gl_Position, normal);
    fragUV = gs_in[0].uv;
    EmitVertex();
    gl_Position = explode(gl_in[1].gl_Position, normal);
    fragUV = gs_in[1].uv;
    EmitVertex();
    gl_Position = explode(gl_in[2].gl_Position, normal);
    fragUV = gs_in[2].uv;

    EmitVertex();
    EndPrimitive();
}