//////////////////////////////////////
//EpiEngine High Range Dynamic Lighting Shader
//Author: Asper Arctos
//Date: 16/2/2015
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;

const int hdrSamples = 10;
const float hdrStrength = 0.32;

float getIntensity(vec4 col)
{
    return (col.r + col.g + col.b) / 3;
}

float getScreenCoordinate(int sample)
{
    return (1.0/hdrSamples)*sample;
}

void main()
{
    vec4 pixelColor = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);
    float pixelIntensity = getIntensity(pixelColor);
    
    float totalIntensity = 0.0;
    
    for (int i = 0; i<hdrSamples; i++)
    {
        for (int j = 0; j<hdrSamples; j++)
        {
            vec2 coord = vec2(getScreenCoordinate(i), getScreenCoordinate(j));
            totalIntensity += getIntensity(texture2D(bgl_RenderedTexture, coord));
        }
    }
    
    float averageIntensity = totalIntensity/(hdrSamples*hdrSamples);
    
    float diff = pixelIntensity - averageIntensity;
    
    gl_FragColor = pixelColor - (diff*hdrStrength);
    gl_FragColor.a = 1.0;
}