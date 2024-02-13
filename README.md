# rooster-epd
With this you can show your Zermelo schedule on an E-Paper display.
Front | Back | USB port
:--:|:--:|:--:
![Front](/Images/epd_front.png) | ![Back](/Images/epd_back.png) | ![USB](/Images/epd_usb.png)

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
1. Follow [this article](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/0) to install Thonny onto your computer and install MicroPython onto your Raspberry Pi Pico
2. Open `main.py` with Thonny
3. Click on "`File`->`Save as`"
4. On the "Where to save to?" prompt click on `MicroPython device`

   ![Thonny "Where to save to?"](/Images/thonny_save.png)

5. Unplug the Raspberry Pi Pico
6. Plug the Raspberry Pi Pico into the E-Paper display and make sure it is facing the right way

   Tip: On the E-Paper display is a "USB" marking

   ![E-Paper display](/Images/epaper_display.png)

### Setting up the computer side
1. Go to the Zermelo zportal of your school
2. Click on `Instellingen`
   
   ![Zermelo](/Images/zermelo_home.png)
3. Then click on `Koppel externe applicatie`
   
   ![Zermelo instellingen](/Images/zermelo_settings.png)
4. Make note of the "Schoolnaam" and "Koppelcode" as shown in the image
   
   ![Zermelo koppel externe applicatie](/Images/zermelo_koppel_externe_app.png)
5. Run `Rooster_epd.exe` or `rooster_epd.pyw`
6. Enter the "Schoolnaam" and "Koppelcode" into their respective fields and click on save
   
   ![Setup window](/Images/setup_window.png)

   Note: This screen can popup again, this means that Zermelo has logged you out on all of your devices. This is normal, Zermelo does that each year I think. If it happens you only have to enter a new "Koppelcode", the "Schoolnaam" is saved for your convenience.
7. Enter the start time of your first possible lesson and the end time of your last possible lesson into their respective fields and click on save

    ![Tijden window](/Images/tijden_window.png)

   Note: In the example above the first possible lesson (u1) starts at 8:30 and the last possible lesson (u9) ends at 16:10

## Usage
Note: The order is important, otherwise the Raspberry Pi Pico won't be detected in the software
1. Connect the Raspberry Pi Pico with the E-Paper display to the computer
2. Run `Rooster_epd.exe` or `rooster_epd.pyw`
3. Select the port that the Rapsberry Pi Pico is connected to

   ![Main window](/Images/main_window.png)

   Note: If you connected the Raspberry Pi Pico after running the software you need to click on "`Instellingen`->`Refresh ports`" before you can select the port
4. If you want to add notes click on "`Notities`->`Notities bewerken`", add your notes and click on save

   ![Main window](/Images/notities_window.png)
5. Click on `Vandaag` or `Morgen` depending on which day you'd like to upload
6. Wait until the led on the Raspberry Pi Pico turns off
7. Unplug the Raspberry Pi Pico


## Useful links
### Required python modules for the source code
- https://pypi.org/project/pyserial/
- https://pypi.org/project/zermelo.py/
- https://pypi.org/project/PySide6/
### Other links
- https://github.com/wouter173/zermelo.py
- https://stackoverflow.com/questions/76138267/read-write-data-over-raspberry-pi-pico-usb-cable
- https://note.nkmk.me/en/python-unix-time-datetime/#convert-unix-time-epoch-time-to-datetime-fromtimestamp
