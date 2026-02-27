#version 330

in vec2 in_pos;  
in vec3 in_color;

uniform mat4 model;       
uniform mat4 projection; 
uniform mat4 view; 

out vec3 myColor;

void main() {
    gl_Position = projection * view * model * vec4(in_pos, 0.0, 1.0);
    myColor = in_color;
}