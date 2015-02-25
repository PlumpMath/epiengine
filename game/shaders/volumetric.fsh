//////////////////////////////////////
//EpiEngine Volumetric Lighting Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;

float volumetricStrength = 0.006;
float volumetricThreshold = 0.65;
int volumetricSamples = 40;

void main()
{
    //Get values
    vec2 coord = gl_TexCoord[0].st;
	vec4 color = texture2D(bgl_RenderedTexture, coord);
    
    //Hunt light source
    float xD = ((coord.x - 0.5)/volumetricSamples);
    float yD = ((coord.y - 0.5)/volumetricSamples);
    
    vec4 sourceColor = vec4(0.0);
    
    for (int i = 0; i<volumetricSamples; i++)
    {
        float x = coord.x - i*xD;
        float y = coord.y - i*yD;
        
        vec2 sCoord = vec2(x, y);
        vec4 sColor = texture2D(bgl_RenderedTexture, sCoord);
        float sPower = (sColor.r + sColor.g + sColor.b)/3;
        
        if (x < 0 || y < 0 || y > 1 || x > 1)
        {
            continue;   
        }
        
        if (sPower > volumetricThreshold)
        {
            sourceColor += sPower * sColor;
        }
    }
    
    gl_FragColor = color + (sourceColor/(1/volumetricStrength));
    gl_FragColor.a = 1.0;
} 