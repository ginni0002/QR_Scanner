QR_Scanner is a helper function I designed while being part of a club. This was my first contribution that I solely worked on.
Although this is not the exact same code as I first implemented but I've decided to split it into parts which makes more sense rather than a big jumbled up file.

How it works:
Can either create another test file to import qr_scanner.py and use the detect function directly or pass an absolute file path as a command line argument to qr_scanner.py.

1. The file path is read and image is loaded from the file path using cv2.
2. The image is converted to grayscale, passed through a gaussian blur filter.
3. Canny edge detection is used to find edges of the qr code position markers.
4. From the edges, we find contours with a nested heirarchy of >5 indicating a position marker.
5. Then we draw bounding boxes over the position markers and calculate the left, right, top and bottom coordinates.
6. Adding a padding of 30% to these coordinates, we form a bounding box over the qr code.
7. Look out for clipping of the qr code over any edge.
8. Finally, decode the qr code into a string

