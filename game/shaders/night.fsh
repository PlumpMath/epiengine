//////////////////////////////////////
//EpiEngine Night Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;

float nightQuality = 1.0;

void main()
{
    //Get values
    vec2 coord = gl_TexCoord[0].st;
	vec4 color = texture2D(bgl_RenderedTexture, coord);

    vec4 fl = vec4((color.r + color.g + color.b)/3);
    
    float strength = nightQuality * fl * 2;
    
    gl_FragColor = mix(fl, color, vec4(strength));
    gl_FragColor.a = 1.0;
} 