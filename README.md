# rooster-epd
With this you can show your Zermelo schedule on an E-Paper display.
Front | Back | USB port
:--:|:--:|:--:
![](/Images/epd_front.png) | ![](/Images/epd_back.png) | ![](/Images/epd_usb.png)

## Required materials
- [Raspberry Pi Pico with wifi and headers](https://www.raspberrystore.nl/PrestaShop/nl/raspberry-pi-pico/486-raspberry-pi-pico-wh-5056561800196.html)
- [Waveshare 2.66inch E-Paper E-Ink Display Module (B) for Raspberry Pi Pico](https://www.waveshare.com/pico-epaper-2.66-b.htm)
- Micro USB cable
### Optional
- 3D Printed case - [STL files in releases](https://github.com/duisterethomas/rooster-epd/releases)

  _Note: If you want to be able to see the led light I recommend to print it in white PLA_
- 4x M2.5 x 6 screws - (I bought [this kit](https://www.amazon.nl/dp/B075WY5367?psc=1&ref=ppx_yo2ov_dt_b_product_details))

## First time setup
First download the [latest release](https://github.com/duisterethomas/rooster-epd/releases) or clone the source code
   
### Setting up your Raspberry Pi Pico
1. Follow [this article](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/0) to install Thonny onto your computer and install MicroPython onto your Raspberry Pi Pico
2. Follow [this article](https://www.freva.com/transfer-files-between-computer-and-raspberry-pi-pico/) to copy all files in `Pico code` to your Raspberry Pi Pico
3. Unplug the Raspberry Pi Pico
4. Plug the Raspberry Pi Pico into the E-Paper display and make sure it is facing the right way

   _Tip: The E-Paper display has a "USB" marking_

   ![](/Images/epaper_display.png)

### Setting up the computer side
First you need to connect to Zermelo
1. Go to the Zermelo zportal of your school
2. Click on `Instellingen`
   
   ![](/Images/zermelo_home.png)
3. Then click on `Koppel externe applicatie`
   
   ![](/Images/zermelo_settings.png)
4. Make note of the "Schoolnaam" and "Koppelcode" as shown in the image
   
   ![](/Images/zermelo_koppel_externe_app.png)
5. Connect the Raspberry Pi Pico with the E-Paper display to the computer
6. Run `Rooster_epd.exe` or `rooster_epd.pyw`
7. Select the port that the Rapsberry Pi Pico is connected to

   ![](/Images/main_window.png)

   _Note: If you connected the Raspberry Pi Pico after running the software you need to click on "`Instellingen`->`Refresh ports`" before you can select the port_
8. Click on `Connect`
9. Click on "`Instellingen`->`Zermelo koppelen`"
10. Enter the "Schoolnaam" and "Koppelcode" into their respective fields
    
    ![](/Images/setup_window.png)

    _Note: This screen can popup again when running this software after some time, this means that Zermelo has logged you out on all of your devices. This is normal, Zermelo does that each year I think. If it happens you only have to enter a new "Koppelcode", the "Schoolnaam" is saved for your convenience._

11. Click on `Opslaan`

Now it's time to add your Wi-Fi networks
1. Click on "`Instellingen`->`Wi-Fi netwerken`"
2. Add all of your Wi-Fi networks that you want to use by clicking on `Nieuw Wi-Fi netwerk` and filling in the wifi credentials

    ![](/Images/wifi_window.png)
  
3. Click on `Opslaan`

Then you need to set up the lesson times
1. Click on "`Instellingen`->`Tijden bewerken`"
2. Enter the start time of your first possible lesson and the end time of your last possible lesson into their respective fields

    ![](/Images/tijden_window.png)

   _Note: In the example above the first possible lesson (u1) starts at 8:30 and the last possible lesson (u9) ends at 16:10_

3. Click on `Opslaan`

## Basic usage
To sync the display with your Zermelo schedule connect the Pico to any usb power source like a usb charger or powerbank and wait for the light to turn off. When the light turns off you can safely disconnect the power again. Note that when you connect it to a computer it won't sync automatically, you will need to sync it via `Rooster_epd.exe` or `rooster_epd.pyw` with the `Sync` button.

If it doesn't work when plugging into a usb power source like a usb charger or powerbank, try plugging it in again, sometimes the WiFi connection fails. If that doesn't work plug Pico into a computer and run `Rooster_epd.exe` or `rooster_epd.pyw`. If the `Zermelo koppelen` window pops up, the Zermelo token has expired so you need to get a new "Koppelcode". If nothing pops up check the wifi settings under "`Instellingen`->`Wi-Fi netwerken`".

## Changing setings
To change any settings, add appointments or add notes you need to first follow the following steps
1. Connect the Raspberry Pi Pico with the E-Paper display to the computer
2. Run `Rooster_epd.exe` or `rooster_epd.pyw`
3. Select the port that the Rapsberry Pi Pico is connected to

   ![](/Images/main_window.png)

   _Note: If you connected the Raspberry Pi Pico after running the software you need to click on "`Instellingen`->`Refresh ports`" before you can select the port_
4. Click on `Connect`

### Adding notes
1. Click on "`Bewerken`->`Notities bewerken`"

   ![](/Images/notities_window.png)
2. Add your notes
3. Click on `Opslaan` to upload your notes to the epd
4. Click on `Sync` to sync the display if necessary

### Adding appointments
1. Click on "`Bewerken`->`Afspraken bewerken`"

   ![](/Images/afspraken_window.png)
2. If you want to add/edit templates click on the arrow next to `Nieuwe afspraak` and select `Sjablonen bewerken`

   ![](/Images/sjablonen_window.png)
3. From there you can add a new template by clicking on `Nieuw sjabloon` and/or edit existing templates

   _Note: Entering the name of the template is required, the rest is optional_
4. When you are done editing templates click on `Opslaan`
5. To add an appointment either click on `Nieuwe afspraak` to add an empty appointment or click on the arrow next to `Nieuwe afspraak` and select one of your templates
6. When you are done adding appointments click on `Opslaan`
7. Click on `Sync` to sync the display if necessary

## Useful links
### Required python modules for the source code
- https://pypi.org/project/pyserial/
- https://pypi.org/project/zermelo.py/
- https://pypi.org/project/PySide6/
### Other links
- https://github.com/wouter173/zermelo.py
- https://stackoverflow.com/questions/76138267/read-write-data-over-raspberry-pi-pico-usb-cable
- https://note.nkmk.me/en/python-unix-time-datetime/#convert-unix-time-epoch-time-to-datetime-fromtimestamp
