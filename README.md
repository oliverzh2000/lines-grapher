# lines.exe

### CMD line usage: 
lines.exe 'image name' (optional) 'scale'

### Example: 
lines.exe mylittlepony.jpg 25
This opens the file mylittlepony.jpg, from the same directory as lines.exe.
The outputted lines will correspond to a picture on desmos that is centered about (0, 0) 
and vertically spans 25 units up and 25 units down.
Defualt scale is 1.

### Instructions:
+ '+' and '-' to zoom
+ Arrows keys to pan
+ Left click to set the endpoint of a line segment beginning from the previous click.
+ shift-click to set the begin point of a brand new line segment. Use this to jump
to another section in the image without a connecting line
ctrl-Z to erase the last line. Make sure the next click is shift click.
+ Press esc to exit. The program will create a new txt file containing all the
lines segments. Use lines_clipboard.exe to copy it into desmos quickly.

# lines_clipboard.exe
### CMD line usage
lines_clipboard.exe 'filename'

### Example: 
lines_clipboard.exe lines_2017-11-30_17-57-14.txt

### Instructions:
+ The program will read the file line by line and place the current line in your clipboard (ctrl-C).
+ Paste the current line into desmos and press enter to advance to the next line.
