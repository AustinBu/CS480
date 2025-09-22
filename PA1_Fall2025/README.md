Austin Bu
CS 480
PA1

Completed drawLine and drawTriangle methods, with color smoothing and antialiasing.
- For drawLine, used bresenham, with an additional check to swap the x and y coordinates to ensure slope <= 1
- For drawTriangle, used bilinear interpolation, then used draw line between the points
- For color smoothing, used linear and bilinear interpolation
- For AA, ran bresenham on a new line that had base coordinated multiplied by the AA level, used dictionaries to track opacity and color