#version 420 core

out vec4 outColor;

const float EPSILON  = 1e-5;
const float INFINITY = 1e5;

uniform vec3 Background;
uniform vec2 resolution;

uniform vec3 cameraU;
uniform vec3 cameraV;
uniform vec3 cameraW;
uniform vec3 cameraEye;
uniform float fov;

uniform vec3 minBound; // Scene bound
uniform vec3 maxBound;


struct Ray
{
    vec3 origin;
    vec3 direction;
    float tMin, tMax;
};

vec3 pointOnRay(in Ray ray,float t){
    return (ray.origin+t*ray.direction);
}

struct AABB{
    vec3 minP;
    vec3 maxP;
};



Ray getRay(vec2 pixel){
    Ray ray;
    ray.origin = cameraEye;
    float height = 2.*tan(fov/2.);
    float aspect = resolution.x/resolution.y;
    float width = height*aspect;
    vec2 windowDim = vec2(width,height);
    vec2 pixelSize = windowDim/resolution;
    vec2 delta = -0.5*windowDim + pixel*pixelSize;
    ray.direction = -cameraW + cameraV*delta.y + cameraU*delta.x;
    ray.tMin = 0.;
    ray.tMax = INFINITY;
    return ray;
}


bool insersectsRayAABB(inout Ray ray, AABB aabb) {
    vec3 tMin = (aabb.minP.xyz - ray.origin) / ray.direction;
    vec3 tMax = (aabb.maxP.xyz - ray.origin) / ray.direction;
    vec3 t1 = min(tMin, tMax);
    vec3 t2 = max(tMin, tMax);
    float tNear = max(max(max(t1.x, t1.y), t1.z),ray.tMin);
    float tFar  = min(min(min(t2.x, t2.y), t2.z),ray.tMax);
    //float tNear = max(max(t1.x, t1.y), t1.z);
    //float tFar  = min(min(t2.x, t2.y), t2.z);
    if (tNear < tFar){
        ray.tMin = tNear;
        ray.tMax = tFar;
        return true;
    }
    return false;
}


vec3 getNormal(AABB aabb,vec3 p){
    vec3 c = (aabb.minP+aabb.maxP)/2.;
    vec3 dim = (aabb.maxP-aabb.minP)/2.;
    vec3 d = (p-c)/dim;
    vec3 v = abs(d);
    int i = v.y > v.x ? ( v.z > v.y ? 2 : 1 ) : ( v.z > v.x ? 2 : 0 );

    // Which Sign of the axis: The sign of the component selects the positive or negative direction.
    return (i == 0) ? ((p.x>=0.)?vec3(1,0,0):vec3(-1,0,0)) :
            (i == 1) ? ((p.y>=0.)?vec3(0,1,0):vec3(0,-1,0)) :
            ((p.z>=0.)?vec3(0,0,1):vec3(0,0,-1));
}

vec3 pixelColor(vec2 pixel){
    vec3 color = Background;
    Ray ray = getRay(pixel);
    AABB aabb;
    aabb.minP = minBound;
    aabb.maxP = maxBound;
    if (insersectsRayAABB(ray, aabb)){
        vec3 p = pointOnRay(ray,ray.tMin);
        vec3 N = getNormal(aabb,p);
        return (N+1.)/2.;
    }
    return Background;
}


void main() {
    outColor = vec4(pixelColor(gl_FragCoord.xy),1.0);
}


//void main() {
//    vec2 uv = gl_FragCoord.xy / resolution.xy;
//    outColor = vec4(uv.x, uv.y, 0.0, 1.0);
//
////    outColor = vec4(vec3(resolution.x),1.0);
//}