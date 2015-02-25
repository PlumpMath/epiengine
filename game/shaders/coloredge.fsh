//////////////////////////////////////
//EpiEngine Color Based Edge Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;
uniform sampler2D bgl_DepthTexture;

float edgeThreshold = 0.01;
vec4 edgeColor = vec4(0.0, 0.0, 0.0, 1.0);
float edgeSearchRange = 0.005;

float getDifference(vec4 color1, vec4 color2)
{
    return abs(((color1.r + color1.g + color1.b)/3) - ((color2.r + color2.g + color2.b)/3));
}

void main()
{
    //Get values
    vec2 coord = gl_TexCoord[0].st;
	vec4 color = texture2D(bgl_RenderedTexture, coord);
    float depth = texture2D(bgl_DepthTexture, coord).x;
    
    //Check border amount
    vec2 sCoord = vec2(coord.x+edgeSearchRange, coord.y);
    vec4 sColor = texture2D(bgl_RenderedTexture, sCoord);
    
    float diffX = getDifference(color, sColor);
        
    sCoord = vec2(coord.x, coord.y+edgeSearchRange);
    sColor = texture2D(bgl_RenderedTexture, sCoord);
    
    float diffY = getDifference(color, sColor);
    
    if (diffX > edgeThreshold || diffY > edgeThreshold)
    {
        color = edgeColor;
    }
    
    gl_FragColor = color;
    gl_FragColor.a = 1.0;
} 