# Rooster-EPD V3
A small e-Paper device that shows your Zermelo schedule.

## Required materials
- [Raspberry Pi Zero 2WH](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
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
## Installing Raspberry Pi OS
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
   - The keyboard layout isn't very important, but useful if anything fails and you need to connect a keyboard to the Pi itself
8. Set a Username and Password and click `NEXT`
   - **Remember these as you will need them later on!**
9. Enter your Wi-Fi SSID and Password and click `NEXT`
10. Turn `Enable SSH` on, select `Use password authentication` and click `NEXT`
11. Turn `Enable Raspberry Pi Connect` off and click `NEXT`
12. Click `WRITE`, wait a couple of seconds, click `I UNDERSTAND, ERASE AND WRITE` and wait for the Imager to finish
13. Once it's finished you have to go into the `bootfs` partition of the sd card, edit `cmdline.txt` and add ` brcmfmac.feature_disable=0x2282000` to the end of the first line
    - This is because of a bug currently somewhere in Raspberry Pi OS that causes the Wi-Fi to not work correctly, so this fixes that
14. Finally you can eject the Micro SD card and put it in the Rasberry Pi

## Installing Rooster-EPD on the Raspberry Pi
1. Plug the Micro USB cable into the `PWR IN` port on the Raspberry Pi and plug it into your USB power supply and wait for it to boot and set itself up
   - You can check if it is done by entering `ping HOSTNAME` where `HOSTNAME` is the hostname you set earlier, so in my case `ping rooster-epd`. If you get succesful ping results it's done and online
2. Connect to the Raspberry Pi via SSH by running `ssh USERNAME@HOSTNAME` in a terminal where `USERNAME` is the username you set earlier and `HOSTNAME` is the hostname you set earlier, in my case `ssh thomas@rooster-epd`. After that enter the password you set earlier
3. Make sure the  Raspberry Pi is up to date by running `sudo apt update` and then `sudo apt upgrade`
4. Download the latest release by running `wget https://github.com/duisterethomas/rooster-epd/download/V3.1.0/rooster-epd_3.1.0-1_all.deb`
5. Install the package by running `sudo apt install ./rooster-epd_3.1.0-1_all.deb`
6. Reboot by running `sudo reboot` and everything should be working!

## Adding more Wi-Fi networks (optional)
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

# Building the .deb package
Run these commands in the root of the repo:
```bash
sudo apt install git debhelper dh-virtualenv build-essential python3-dev python3-venv python3-pip python3-wheel python3-pil
git clone https://github.com/duisterethomas/rooster-epd.git
cd rooster-epd
dpkg-buildpackage -b -uc
```

# Useful links
- https://github.com/wouter173/zermelo.py
- https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(G)_Manual#Raspberry_Pi
- https://github.com/Bananattack/omelette_font
- https://nicegui.io/documentation
