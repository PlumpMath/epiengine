//////////////////////////////////////
//EpiEngine Depth Based Edge Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;

float edgeThreshold = 0.001;
vec4 edgeColor = vec4(0.0, 0.0, 0.0, 1.0);
float edgeSearchRange = 0.005;

void main()
{
    //Get values
    vec2 coord = gl_TexCoord[0].st;
	vec4 color = texture2D(bgl_RenderedTexture, coord);
    float depth = texture2D(bgl_DepthTexture, coord).x;
    
    //Check border amount
    vec2 sCoord = vec2(coord.x+edgeSearchRange, coord.y);
    float sDepth = texture2D(bgl_DepthTexture, sCoord).x;
    
    float diffX = abs(depth - sDepth);
   
    sCoord = vec2(coord.x, coord.y+edgeSearchRange);
    sDepth = texture2D(bgl_DepthTexture, sCoord).x;
    
    float diffY = abs(depth - sDepth);
    
    if (diffX > edgeThreshold || diffY > edgeThreshold)
    {
        color = edgeColor;
    }
    
    gl_FragColor = color;
    gl_FragColor.a = 1.0;
} 