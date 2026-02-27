#version 330
in float myColor;

out vec4 fragColor;             

void main() {
    fragColor = vec4(myColor, myColor, 1.0, 1.0); 
}