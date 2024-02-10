# Pico code
main.py is the code that you need to flash to the raspberry pi pico.

## Pico commands
- `init`: Initializes the display
- `rectCXXXYYYWWWHHHF`: Rectangle

  `C`: The colour (r/b/w)
  
  `XXX`: X position
  
  `YYY`: Y position
  
  `WWW`: Width
  
  `HHH`: Height
  
  `F`: Filled (0/1)

  Filled black rectangle on x 2, y 2, width 30, height 30 example: `rectb0020020300301`
- `textCXXXYYYTEXT`: Text

  `C`: The colour (r/b/w)
  
  `XXX`: X position
  
  `YYY`: Y position
  
  `TEXT`: The text

  Red "Hello, world!" on x 2 and y 2 example: `textr002002Hello, world!`
- `show`: Shows the final result
- `cancel`: Cancel
