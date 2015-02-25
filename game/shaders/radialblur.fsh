//////////////////////////////////////
//EpiEngine Radial Blur Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;

const int radialBlurSamples = 10;
const float radialBlurOffsetX = -0.5;
const float radialBlurOffsetY = -0.5;
const float radialBlurStrength = 0.003;

float rand(vec2 co)
{
    return fract(sin(dot(co ,vec2(12.9898,78.233))) * 43758.5453);
}

void main()
{
    //Get values
    vec2 coord = vec2(gl_TexCoord[0]).st;
    coord = vec2(abs(coord.st.x+radialBlurOffsetX), abs(coord.st.y+radialBlurOffsetY));
    
    float diff = sqrt(pow(coord.x, 2) + pow(coord.y, 2));
    
    //Blur
    vec4 color = vec4(0.0);
    
    for (int i = 0-(radialBlurSamples)/2; i < radialBlurSamples/2; i++)
    {
        float x = gl_TexCoord[0].x  + (diff * i * radialBlurStrength * rand(coord));
        float y = gl_TexCoord[0].y  + (diff * i * radialBlurStrength * rand(coord));
        color += texture2D(bgl_RenderedTexture, vec2(x, y));
    }
    
    color /= radialBlurSamples;
    
    gl_FragColor = color;
    //gl_FragColor = vec4(diff);
    gl_FragColor.a = 1.0;
} 