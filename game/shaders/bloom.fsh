//////////////////////////////////////
//EpiEngine Bloom Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_LuminanceTexture;

float bloomSearchFactor = 0.002;
float bloomColorFactor = 0.005;
int bloomSamples = 10;

void main()
{
    //Get values
    vec2 coord = vec2(gl_TexCoord[0]);
    
    //Average bloom
    vec4 sum = vec4(0.0);
    
    for (int i = -bloomSamples; i < bloomSamples; i++)
    {
        for (int j = -bloomSamples; j < bloomSamples; j++)
        {
            vec2 cCoord = coord + (vec2(j, i) * bloomSearchFactor);
            vec4 cColor = texture2D(bgl_RenderedTexture, cCoord);
            
            float cPower = cColor.x + cColor.y + cColor.z;
            
            sum += cColor * cPower * bloomColorFactor;
        }
    }
    
    gl_FragColor =  texture2D(bgl_RenderedTexture, coord) + (sum/bloomSamples);
} 