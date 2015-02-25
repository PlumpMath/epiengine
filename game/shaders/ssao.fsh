//////////////////////////////////////
//EpiEngine Screen Space Ambient Occlusion Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;

int ssaoSamples = 3;
int ssaoRings = 2;
float ssaoSampleRange = 6.0;
float ssaoFarLimit = 100.0;
float ssaoNearLimit = 0.1;
float ssaoMultiplier = 25.0;

float step = 3.14159*2.0/float(ssaoSamples);

vec4 threshold = vec4(0.2, 0.2, 0.2, 0.2);

float rand(vec2 coord)
{
    return fract(sin(dot(coord ,vec2(12.9898,78.233))) * 43758.5453);
}

float calculateAO(vec2 coord)
{
    float ao = 0.0;
    
    float depth = texture2D(bgl_DepthTexture, coord).x;
    
    for (int i = 0; i<ssaoRings; i++)
    {
        for (int j = 0; j<ssaoSamples; j++)
        {
			float px = cos(float(j)*step)*float(i);
			float py = sin(float(j)*step)*float(i);
            
            vec2 sCoord = vec2(coord.s+px+rand(coord), coord.t+py+rand(coord));
            
            float sDepth = texture2D(bgl_DepthTexture, sCoord).x;
            
            float depthDiff = depth - sDepth;
            
            depthDiff = sqrt(clamp(1.0-(depthDiff)/(ssaoSampleRange/(ssaoFarLimit-ssaoNearLimit)), 0.0, 1.0));
            
            ao += min(1.0, max(0.0, depth - sDepth) * ssaoMultiplier) * depthDiff;
        }
    }
    
    ao /= ssaoRings*ssaoSamples;
    
    return 1.0 - ao;
}

void main()
{
    //Get values
    vec2 coord = gl_TexCoord[0].st;
	vec4 color = texture2D(bgl_RenderedTexture, coord);
    float luminance = (color.r + color.g + color.b) / 3;
    
    float ao = calculateAO(coord);
    
    gl_FragColor = color * mix(vec4(luminance), vec4(1.0), vec4(ao));
    gl_FragColor.a = 1.0;
} 