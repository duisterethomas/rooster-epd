# rooster-epd
With this you can show your Zermelo schedule on an E-Paper display.

## Required materials
- [Raspberry Pi Pico with headers](https://www.raspberrystore.nl/PrestaShop/nl/raspberry-pi-pico/471-raspberry-pi-pico-h.html)
- [Waveshare 2.66inch E-Paper E-Ink Display Module (B) for Raspberry Pi Pico](https://www.waveshare.com/pico-epaper-2.66-b.htm)
- Micro USB cable
### Optional
- 3D Printed case - [STL files in releases](https://github.com/duisterethomas/rooster-epd/releases)

  Note: If you want to be able to see the led light I recommend to print it in white PLA
- 4x M2.5 x 6 screws - (I bought [this kit](https://www.amazon.nl/dp/B075WY5367?psc=1&ref=ppx_yo2ov_dt_b_product_details))

## First time setup
First download the [latest release](https://github.com/duisterethomas/rooster-epd/releases) or clone the source code
   
### Setting up your Raspberry Pi  Pico
1. Follow [this article](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/0) to install Thonny and install MicroPython onto your Raspberry Pi Pico
2. Open `/Pico code/main.py` with Thonny
3. Click on "`File`->`Save as`"
4. On the "Where to save to?" prompt click on `MicroPython device`

   ![Thonny "Where to save to?"](/Images/thonny_save.png)

### Setting up the computer side
1. Go to the Zermelo zportal of your school
2. Click on `Instellingen`
   
   ![Zermelo](/Images/zermelo_home.png)
3. Then click on `Koppel externe applicatie`
   
   ![Zermelo instellingen](/Images/zermelo_settings.png)
4. Make note of the "Schoolnaam" and "Koppelcode" as shown in the image
   
   ![Zermelo koppel externe applicatie](/Images/zermelo_koppel_externe_app.png)
5. Connect the Raspberry Pi Pico to the computer
6. Run `rooster-epd.exe` or `rooster_epd.py`
7. Enter the "Schoolnaam" and "Koppelcode" into their respective fields and click on save
   
   ![Setup window](/Images/setup_window.png)

   Note: This screen can popup again, this means that Zermelo has logged you out on all of your devices. This is normal, Zermelo does that each year I think. If it happens you only have to enter a new "Koppelcode", the "Schoolnaam" is saved for your convenience.

## Usage
Note: The order is important, otherwise the Raspberry Pi Pico won't be detected in the software
1. Connect the Raspberry Pi Pico to the computer
2. Run `rooster-epd.exe` or `rooster_epd.py`
3. Select the port that the Rapsberry Pi Pico is connected to

   ![Main window](/Images/main_window.png)

   Note: The port is saved for your convenience, so you don't have to select it every time you run the program.
5. Finally click on `Vandaag` or `Morgen` depending on which day you'd like to upload


## Useful links
### Required python modules for the source code
- https://pypi.org/project/pyserial/
- https://pypi.org/project/zermelo.py/
- https://pypi.org/project/PySide6/
### Other links
- https://github.com/wouter173/zermelo.py
- https://stackoverflow.com/questions/76138267/read-write-data-over-raspberry-pi-pico-usb-cable
- https://note.nkmk.me/en/python-unix-time-datetime/#convert-unix-time-epoch-time-to-datetime-fromtimestamp
