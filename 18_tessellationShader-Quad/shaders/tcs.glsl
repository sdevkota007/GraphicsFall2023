#version 420 core

layout (vertices = 4) out;

uniform int outerLevel0;
uniform int outerLevel1;
uniform int outerLevel2;
uniform int outerLevel3;

uniform int innerLevel0;
uniform int innerLevel1;

void main()
{
    gl_TessLevelOuter[0] = outerLevel0;
    gl_TessLevelOuter[1] = outerLevel1;
    gl_TessLevelOuter[2] = outerLevel2;
    gl_TessLevelOuter[3] = outerLevel3;

    gl_TessLevelInner[0] = innerLevel0;
    gl_TessLevelInner[1] = innerLevel1;

    gl_out[ gl_InvocationID ].gl_Position = gl_in[ gl_InvocationID ].gl_Position;
}

