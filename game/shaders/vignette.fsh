//////////////////////////////////////
//EpiEngine Vignette Shader
//Author: Asper Arctos
//Date: 18/12/2014
//////////////////////////////////////
uniform sampler2D bgl_RenderedTexture;

const float vignetteSize = 1.0;
const float vignetteFactor = 1.25;
const float vignetteOffsetX = -0.5;
const float vignetteOffsetY = -0.5;

vec2 getAbsCentredCoordinates(vec2 coord)
{
    vec2 adjusted = vec2(abs(coord.st.x+vignetteOffsetX), abs(coord.st.y+vignetteOffsetY));
    return pow(adjusted, vec2(2.0));
}

float getGradient(vec2 centreCoord)
{
    return smoothstep(vignetteSize-vignetteFactor, vignetteSize+vignetteFactor, centreCoord.x + centreCoord.y);
}

void main()
{
    //Get values
    vec2 centreCoord = getAbsCentredCoordinates(gl_TexCoord[0].st);
    
    //Get colors
    vec4 originalColor = texture2D(bgl_RenderedTexture, gl_TexCoord[0].st);
    float colorAlteration = getGradient(centreCoord);
    
    //Mix colors
    gl_FragColor = mix(originalColor, vec4(0.0), colorAlteration);
    gl_FragColor.a = 1.0;
}