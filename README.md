# Rooster-EPD V3
A small e-Paper device that shows your Zermelo schedule.

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
- An SSH client, I use OpenSSH
- Any SFTP client, I use [FileZilla](https://filezilla-project.org/)

## Setting up the Pi
### Installing Raspberry Pi OS
1. Download and install [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Insert the Micro SD card and run Raspberry Pi Imager
3. Select `Raspberry Pi Zero 2 W` and click `NEXT`
   - Select `Raspberry Pi Zero W` if you use that one
4. Select `Raspberry Pi OS (other)` and then `Raspberry Pi OS Lite (64-bit)` and click `NEXT`
   - Select `Raspberry Pi OS Lite (32-bit)` if you use a Raspberry Pi Zero W
5. Select your Micro SD card and click `NEXT`
6. Enter a hostname and click `NEXT`, I set it to `rooster-epd`
   - **Remember this as you will need it later on!**
7. Set the `National capital`, `Time zone` and `Keyboard layout` and click `NEXT`
   - The keyboard layout isn't very important, but useful if anything fails and you need to connect a keyboard to the pi itself
8. Set a username and password and click `NEXT`
   - **Remember these as you will need them later on!**
9. Enter your Wi-Fi SSID and Password and click `NEXT`
10. Turn `Enable SSH` on, select `Use password authentication` and click `NEXT`
11. Turn `Enable Raspberry Pi Connect` off and click `NEXT`
12. Click `WRITE`, wait a couple of seconds, click `I UNDERSTAND, ERASE AND WRITE` and wait for the Imager to finish
13. Once it's finished you have to go into the `bootfs` partition of the sd card, edit `cmdline.txt` and add `brcmfmac.feature_disable=0x2282000` to the end of the first line
    - This is because of a bug currently somewhere in Raspberry Pi OS that causes the wifi to not work correctly, so this fixes that
14. Finally you can eject the Micro SD card and put it in the Rasberry Pi

### Installing Rooster-EPD on the Raspberry Pi
1. Plug the Micro USB cable into the `PWR IN` port on the Raspberry Pi and plug it into your USB power supply and wait for it to boot and set itself up
   - You can check if it is done by entering `ping HOSTNAME` where `HOSTNAME` is the hostname you set earlier, so in my case `ping rooster-epd`. If you get succesful ping results it's done and online
2. Connect to the Pi using your SSH client
   - If you are using OpenSSH like me run `ssh USERNAME@HOSTNAME` in a terminal where `USERNAME` is the username you set earlier and `HOSTNAME` is the hostname you set earlier, in my case `ssh thomas@rooster-epd`. After that enter the password you set earlier
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
    After=network-online.target time-sync.target
    Wants=network-online.target time-sync.target

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
