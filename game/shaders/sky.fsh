varying float x;
varying float y;
varying float z;
uniform sampler2D bgl_RenderedTexture;
uniform float time;

vec4 skyMinimum = vec4(0.1);

vec4 skyColor = vec4(0.2, 0.4, 0.7, 1.0);
float skyPower = 1.0;

vec4 sunColor = vec4(0.9, 0.9, 0.8, 1.0);
vec4 dankColor = vec4(0.5, 0.2, 0.2, 1.0);
float sunPower = 0.15;

const float pi = 3.14159;

vec3 spherePos(vec3 cubePos)
{
    float x = cubePos.x;
    float y = cubePos.y;
    float z = cubePos.z;
    
    float r = pow((pow(x, 2) + pow(y, 2) + pow(z, 2)), 0.5);
    
    float a = x/r;
    float b = y/r;
    float c = z/r;
    
    return vec3(a, b, c);
}

float getDistanceTo(vec3 p1, vec3 p2)
{
    return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2) + pow(p1.z - p2.z, 2));
}

float getSunY(float time)
{
    return (time*2)-1;
}

float getSunZ(float time)
{
    return 1-abs((time*2) - 1);
}

void main()  
{     
    //Get values
    vec2 coord = vec2(gl_TexCoord[0]).st;
    float cx = x;
    float cy = y;
    float cz = z;
    
    float sunY = getSunY(time);
    float sunZ = getSunZ(time);
    vec3 sunPos = spherePos(vec3(0.0, sunY, -sunZ));
    
    vec3 sP = spherePos(vec3(cx, cy, cz));
    
    float height = 1.0 - abs(sP.z);
    float sunDist = getDistanceTo(sunPos, sP);
    sunDist = 7 - ((pow(sunDist, 2)) + (5*sunDist));
    
    float nightPass = 1.0;
    
    if (time > 1.0)
    {
        nightPass -= (time - 1)*2;
    }
    
    //Dusk and dawn
    float dankFactor = 0.0;
    
    if (time < 0.5)
    {
        dankFactor = 0.5 - abs(time);
    }
    else if (time < 1.5)
    {
        dankFactor = 0.5 - abs(1.0-time);
    }
    else if (time < 2.0)
    {
        dankFactor = 0.5 - abs(2.0-time);
    }
    
    vec4 skyPass = skyColor*(height*skyPower);
    vec4 sunPass = sunColor*(sunPower*sunDist);
    vec4 skyBase = skyMinimum;
    vec4 dankPass = dankColor * dankFactor;
    
    if (sunDist < 0.0)
    {
        sunPass = vec4(0.0);
    }
    
    gl_FragColor = (sunPass*dankPass) + (skyPass*nightPass) + skyBase + dankPass;
    gl_FragColor.a = 1.0;
}  