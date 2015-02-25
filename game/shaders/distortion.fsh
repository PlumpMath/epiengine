//////////////////////////////////////
//EpiEngine Distortion Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;

const vec4 distortionRed = vec4(0.5, 0.0, 0.0, 1.0);
const vec4 distortionGreen = vec4(0.0, 0.5, 0.0, 1.0);
const float distortionStrength = 1.0;
const float distortionRange = 0.005;

void main()
{
    //Get values
    vec2 coord = gl_TexCoord[0].st;
    vec4 truecolor = texture2D(bgl_RenderedTexture, coord);

    vec4 color = vec4(0.0);

    //Red
    vec4 leftColor = texture2D(bgl_RenderedTexture, vec2(coord.x+distortionRange, coord.y));
    color += leftColor * distortionRed * distortionStrength;
    
    //Green
    vec4 rightColor = texture2D(bgl_RenderedTexture, vec2(coord.x-distortionRange, coord.y));
    color += rightColor * distortionGreen * distortionStrength;
    
    gl_FragColor = mix(color, truecolor, vec4(0.7));
    gl_FragColor.a = 1.0;
} 