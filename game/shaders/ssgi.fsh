//////////////////////////////////////
//EpiEngine Screen Space Global Illumination Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;

int ssgiSamples = 3;
int ssgiRings = 2;
float ssgiSampleRange = 6.0;
float ssgiFarLimit = 100.0;
float ssgiNearLimit = 0.1;
float ssgiMultiplier = 5.0;

float step = 3.14159*2.0/float(ssgiSamples);

vec4 threshold = vec4(0.2, 0.2, 0.2, 0.2);

float rand(vec2 coord)
{
    return fract(sin(dot(coord ,vec2(12.9898,78.233))) * 43758.5453);
}

float calculateGI(vec2 coord)
{
    float gi = 0.0;
    
    float depth = texture2D(bgl_DepthTexture, coord).x;
    
    for (int i = 0; i<ssgiRings; i++)
    {
        for (int j = 0; j<ssgiSamples; j++)
        {
			float px = cos(float(j)*step)*float(i);
			float py = sin(float(j)*step)*float(i);
            
            vec2 sCoord = vec2(coord.s+px+rand(coord), coord.t+py+rand(coord));
            
            float sDepth = texture2D(bgl_DepthTexture, sCoord).x;
            
            float depthDiff = depth - sDepth;
            
            depthDiff = sqrt(clamp(1.0-(depthDiff)/(ssgiSampleRange/(ssgiFarLimit-ssgiNearLimit)), 0.0, 1.0));
            
            float temp = depthDiff;
            
            vec4 color = texture2D(bgl_RenderedTexture, coord);
            
            float power = (color.r + color.g + color.b)/3;
            
            gi += depthDiff * power;
        }
    }
    
    gi /= ssgiRings*ssgiSamples;
    
    return gi;
}

void main()
{
    //Get values
    vec2 coord = gl_TexCoord[0].st;
	vec4 color = texture2D(bgl_RenderedTexture, coord);
    float luminance = (color.r + color.g + color.b) / 3;
    
    float gi = calculateGI(coord);
    
    gl_FragColor = color + ((1.0 - gi)/ssgiMultiplier);//+ mix(vec4(luminance), vec4(1.0), vec4(gi));
    //gl_FragColor = vec4((1.0 - gi)/ssgiMultiplier);
    gl_FragColor.a = 1.0;
} 