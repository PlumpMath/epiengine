varying float x;
varying float y;
varying float z; 
        
void main()
{
    x = gl_Vertex.x;
    y = gl_Vertex.y;
    z = gl_Vertex.z;
            
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}