# Rooster-EPD V3
With this you can show your Zermelo schedule on an E-Paper display.

## Required materials
- [Raspberry Pi Zero 2WH](https://www.raspberrystore.nl/PrestaShop/nl/raspberry-pi-zero-v1-en-v2/588-raspberry-pi-zero-2wh-5056561800011.html)
  - The original Zero W should also work, however I opted for the Zero 2 W to get better performance
- [Waveshare 2.13inch E-Paper HAT (G), 250x122, Red/Yellow/Black/White, SPI Interface](https://www.waveshare.com/2.13inch-e-paper-hat-g.htm)
- Micro SD card
  - I recommend to get a fast one
  - Size doesn't really matter, 32GB is more than enough
- Micro SD card reader
- Micro USB cable
- USB Power supply / charger

### Optional materials
- 3D Printed case - [STL files in the latest release](https://github.com/duisterethomas/rooster-epd/releases/latest)
- 4x M2.5 x 6 screw - (I bought [this kit](https://www.amazon.nl/dp/B075WY5367))
- 4x M2.5 nut - (Also from [this kit](https://www.amazon.nl/dp/B075WY5367))

# Installation
## Prerequisites
- Any SFTP client, I use [FileZilla](https://filezilla-project.org/)
- Any SSH client, I use the `ssh` command from PowerShell

## Setting up the Pi
### Installing Raspberry Pi OS
1. Download and install [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Insert the Micro SD card and run Raspberry Pi Imager
3. Under `Raspberry Pi Device` select `Raspberry Pi Zero 2 W`
4. Under `Operating System` select `Raspberry Pi OS (other)` and then `Raspberry Pi OS Lite (64-bit)`
5. Under `Storage` select your Micro SD card
6. Click `NEXT`
7. Click `EDIT SETTINGS`
8. Check `Set hostname` and enter a hostname, I set it to `rooster-epd`
   - **Remember this as you will need it later on!**
   - Also note that the final hostname will be what you set + `.local`, so in my case it will be `rooster-epd.local`
9. Check `Set username and password` and enter a username and password
   - **Remember these as you will need them later on!**
10. Check `Configure wireless LAN` and enter your Wi-Fi credentials
    - Don't forget to set the `Wireless LAN country` to your country
11. Check `Set locale settings` and select the right time zone
    - The keyboard layout doesn't matter as we won't be connecting a keyboard.
12. Go to the `SERVICES` tab
13. Check `Enable SSH` and select `Use password authentication`
14. You can set the settings on the `OPTIONS` tab to whatever you like, I disabled telemetry, but that isn't required
15. Click `SAVE`, `YES`, `YES` and wait for the Imager to finish
16. Once it's finished you can take the Micro SD card out and put it in the Rasberry Pi

### Installing required packages on the Raspberry Pi
1. Plug the Micro USB cable into the `PWR IN` port on the Raspberry Pi and plug it into your USB power supply and wait for it to boot and set itself up
   - You can check if it is done by entering `ping HOSTNAME` where `HOSTNAME` is the hostname you set earlier, so in my case `ping rooster-epd.local`. If you get succesful ping results it's done and online
2. Connect to the Pi using your SSH client
   - If you are using PowerShell like me enter `ssh USERNAME@HOSTNAME` where `USERNAME` is the username you set earlier and `HOSTNAME` is the hostname you set earlier, in my case `ssh thomas@rooster-epd.local`. After that enter the password you set earlier
3. Make sure the Pi is up to date by running `sudo apt update` and then `sudo apt upgrade`
4. Now install the required packages using the following commands:
   - `sudo apt install python3-pip`
   - `sudo apt install python3-pil`
   - `sudo apt install python3-numpy`
   - `sudo apt install python3-spidev`
   - `sudo apt install python3-gpiozero`
   - `sudo apt install python3-packaging`
   - `sudo pip3 install nicegui zermelo.py --break-system-packages`
     - Note: `--break-system-packages` hasn't broken anything as far as I've seen with these two packages

### Enabling SPI
Enable the SPI interface of the pi using `sudo raspi-config` and then choose `Interfacing Options` -> `SPI` -> `Yes`

### Installing the python scripts
1. Connect to the Pi using your SFTP client
   - If you are using FileZilla like me enter the hostname in the `Host` field, your username and password in their respective fields, enter `22` in the `Port` field and click `Quickconnect`, then check `Always trust this host, add this key to the cache` and click `Ok`
2. Create a new directory in the home directory of your user called `rooster-epd`, so the full path will be `/home/USER/rooster-epd` where `USER` is your username
3. Download the `Source code (zip)` from the [latest release](https://github.com/duisterethomas/rooster-epd/releases/latest)
4. Unzip it and copy the contents of the `rpi_zero_code` directory into the `rooster-epd` directory you just created on the Pi

### Setting up systemd services
Create the following 2 files and replace `USER` with your username of the Raspberry Pi Zero:
- `/etc/systemd/system/rooster-epd-main.service`
    ```
    [Unit]
    Description=Runs the Rooster-EPD main.py at startup
    After=rooster-epd-screen-refresh.service

    [Service]
    ExecStart=python3 /home/USER/rooster-epd/main.py
    WorkingDirectory=/home/USER/rooster-epd
    Restart=on-failure
    User=USER

    [Install]
    WantedBy=multi-user.target
    ```

- `/etc/systemd/system/rooster-epd-screen-refresh.service`
    ```
    [Unit]
    Description=Runs the Rooster-EPD screen_refresh.py at startup
    After=network-online.target

    [Service]
    ExecStart=python3 /home/USER/rooster-epd/screen_refresh.py
    WorkingDirectory=/home/USER/rooster-epd
    Restart=on-failure
    User=USER

    [Install]
    WantedBy=multi-user.target
    ```

Then enable them with the following commands in this order:
1. `sudo systemctl daemon-reload`
2. `sudo systemctl enable rooster-epd-main.service`
3. `sudo systemctl enable rooster-epd-screen-refresh.service`

### Adding other Wi-Fi networks (optional)
1. Run `sudo nmtui`
2. Select `Edit a connection`
3. Select `<Add>`
4. Enter the `SSID` of the Wi-Fi network
5. Select the right `Security`
   - Most home Wi-Fi networks are `WPA & WPA2 Personal`
     - Then enter the `Password`
   - Most school networks are `WPA & WPA2 Enterprise`
     - Then you must also select the right `Authentication`, in most cases `PEAP`, if not contact your school's network administrators to ask what security is used
       - In the case of `PEAP` enter the `Anoymous identity`, `Username` and `Password`
6. Select `<Ok>`
7. Press escape twice to exit nmtui

### Finalizing the setup
After completing all steps listed above reboot the Pi by running `sudo reboot` via your SSH client. Connect the E-Paper HAT as well if you haven't already.

## Useful links
- https://github.com/wouter173/zermelo.py
- https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(G)_Manual#Raspberry_Pi
- https://github.com/Bananattack/omelette_font
- https://nicegui.io/documentation
