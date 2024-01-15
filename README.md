# rooster-epd
Zermelo rooster op een e-paper schermpje

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

## Useful links
- https://support.zermelo.nl/guides/developers-api/examples/authentication-obtaining-an-access-token#access_token_created_in_the_portal
- https://github.com/wouter173/zermelo.py
- https://pypi.org/project/zermelo.py/
- https://csghetstreek.zportal.nl/app/
- https://stackoverflow.com/questions/76138267/read-write-data-over-raspberry-pi-pico-usb-cable
- https://note.nkmk.me/en/python-unix-time-datetime/#convert-unix-time-epoch-time-to-datetime-fromtimestamp
