Austin Bu
CS480
PA4
This assignment I created four new models: Cylinder, Ellipsoid, Sphere, and Torus
- Used vbo and ebo for coordinates
- I also implemented UV mapping for textures
In Sketch.py, SceneTwo.py, and SceneThree.py I implemented 2 scenes
- The first contains a spotlight
- The second contains an infinite light
- The ability to toggle lights on and off
In FragmentShader.gsl I implemented
- normal rendering, which changes the color of the surface based on the normal direction
- Phong lighting, with specular, diffuse, and ambient
- Infinite, point, and spotlights with radial and angular attenuation
