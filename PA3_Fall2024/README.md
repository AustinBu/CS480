Austin Bu
CS480
PA3
This assignment I created two new models, a frog and a fly (ModelLinkage.py) and allow them to interact with each other.
In Sketch.py I implemented the 2 basic scenarios
In EnviromentObject.py I implemented
- rotateDirection which orients the object in the direction that they are moving
- checkCollision which checks if two objects bounding spheres are overlapping
- reflectDirection which gives an object a new direction if it bumps into the same species
- calculatePotentialForce to give the prey and predator relationship
In ModelLinkage.py I implemented
- Fly, which flies around
- Frog, which frogs around and eats flies