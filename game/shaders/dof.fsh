//////////////////////////////////////
//EpiEngine Depth of Field Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;

float dofBlurMax = 10.0;
float dofBlurFactor = 0.05;
int dofBlurSamples = 10;

vec2 focus = vec2(0.5, 0.5);

float rand(vec2 co)
{
    return fract(sin(dot(co ,vec2(12.9898,78.233))) * 43758.5453);
}

void main()
{
    //Get values
    vec2 coord = vec2(gl_TexCoord[0]).st;
    float depth = texture2D(bgl_DepthTexture, coord).x;
    float focusDepth = texture2D(bgl_DepthTexture, focus).x;
    
    //Compare depths
    float depthDiff = abs(depth - focusDepth) * dofBlurFactor;
    depthDiff = clamp(depthDiff, 0.0, dofBlurMax);
    
    //Blur 
    vec4 color = vec4(0.0);
    
    for (int i = 0; i < dofBlurSamples; i++)
    {
        float x = gl_TexCoord[0].x  + (depthDiff * rand(coord*i));
        float y = gl_TexCoord[0].y  + (depthDiff * rand(coord*i));
        color += texture2D(bgl_RenderedTexture, vec2(x, y));
    }
    
    color /= dofBlurSamples;
        
    //Apply colors
    gl_FragColor = color;
    gl_FragColor.a = 1.0;
}