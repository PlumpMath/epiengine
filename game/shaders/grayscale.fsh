//////////////////////////////////////
//EpiEngine Grayscale Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;

void main()
{
    //Get values
    vec2 coord = gl_TexCoord[0].st;
	vec4 color = texture2D(bgl_RenderedTexture, coord);

    float fl = (color.r + color.g + color.b)/3;
    
    gl_FragColor = vec4(fl);
    gl_FragColor.a = 1.0;
} 