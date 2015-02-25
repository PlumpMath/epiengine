//////////////////////////////////////
//EpiEngine Lens Flare Shader (Broken, do not use).
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;
uniform float bgl_RenderedTextureWidth;
uniform float bgl_RenderedTextureHeight;

float lensFlareThreshold = 0.75;
float lensFlareStrength = 0.05;
float lensFlareSearchRange = 0.11;

int lensFlareSamples = 50;
int lensFlareRings = 1;

float rand(vec2 coord)
{
    return fract(sin(dot(coord ,vec2(12.9898,78.233))) * 43758.5453);
}

void main()
{
    //Get values
    vec2 coord = gl_TexCoord[0].st;
	vec4 color = texture2D(bgl_RenderedTexture, coord);
    
    //Hunt light source
    
    //Calculate search radius
    float deviation = abs(coord.x - 0.5) + abs(coord.y - 0.5);
    float radius = 0.5 - deviation;
    float aspect = 2.0;//FIXME
    
    vec4 sourceColor = vec4(0.0);
    
    for (int i = 1; i<=lensFlareRings; i++)
    {
        for (int j = 0; j<lensFlareSamples; j++)
        {
            //Scale circle
            float angle = ((2*3.14159)/lensFlareSamples)*j;
			float px = coord.s + cos(angle) * (float(i) * radius);
			float py = coord.t + sin(angle) * (float(i) * radius)*aspect;
            
            vec2 sCoord = vec2(px, py);
            vec4 sColor = texture2D(bgl_RenderedTexture, sCoord);
            float sPower = (sColor.r + sColor.g + sColor.b)/3;
            
            if (sPower > lensFlareThreshold)
            {
                sourceColor += sColor;
            }
        }
    }
    
    gl_FragColor = color + (sourceColor/(1/lensFlareStrength));
    //gl_FragColor = sourceColor;
    gl_FragColor.a = 1.0;
} 