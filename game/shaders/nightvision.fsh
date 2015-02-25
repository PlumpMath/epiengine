//////////////////////////////////////
//EpiEngine Night Vision Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;

const vec4 nightVisionColor = vec4(0.4, 0.8, 0.4, 1.0);
const float nightVisionStatic = 0.1;
const float nightVisionBoost = 2.0;
const float nightVisionBarStrength = 0.1;

float rand(vec2 co)
{
    return fract(sin(dot(co ,vec2(12.9898,78.233))) * 43758.5453);
}

void main()
{
    //Get values
    vec2 coord = gl_TexCoord[0].st;
	vec4 color = texture2D(bgl_RenderedTexture, coord);

    float fl = (color.r + color.g + color.b)/3;
    
    fl *= nightVisionBoost;
    
    fl -= rand(coord) * nightVisionStatic;
    
    fl -= nightVisionStatic * mod(coord.y*100, 2) * nightVisionBarStrength;
    
    gl_FragColor = vec4(fl*nightVisionColor);
    gl_FragColor.a = 1.0;
} 