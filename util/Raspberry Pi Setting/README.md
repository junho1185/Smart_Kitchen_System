# Raspberry Pi initial Setting

## git installation

``` 
sudo apt update && sudo apt upgrade
```
```
sudo apt install git
```

## Create SSH Key
```
ssh-keygen -t rsa -b 4096
```
Just press enters afterwards.

View the generated SSH key by the following command.
```
cat /home/pi/.ssh/id_rsa.pub
```

## Clone Repository
Clone this repository.

## Install necesarry libraries
```
pip install -r requirements.txt
```

## Set Default Display

## Disable Double Touch behavior
Modify [input] section in `~/.kivy/config.ini` 
```
[input]
%(name)s = probesysfs,provider=hidinput
mouse = mouse
# mtdev_%(name)s = probesysfs,provider=mtdev 
hid_%(name)s = probesysfs,provider=hidinput
```

## Install MariaDB
Raspberry Pi does not supprt MySQL. Download MariaDB Instead. It works the same.
```
sudo apt update && sudo apt upgrade
```
```
sudo apt install mariadb-server
```
Following `sudo mysql`, run the command below to set the password for root.
```
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
```
Run this command to flush previous data.
```
FLUSH PRIVILEGES;
```
Run this command to enter MySQL(MariaDB)
```
sudo mysql -u root -p
```

## Database initialization
Run the following commands to init database
```
CREATE DATABASE Smart_Kitchen_System;
```
```
USE Smart_Kitchen_System;
```
```
CREATE TABLE RecipeIndex(
  id INT NOT NULL AUTO_INCREMENT,
  foodName VARCHAR(20) NOT NULL,
  region INT NOT NULL,
  PRIMARY KEY(id)
);
```
```
CREATE TABLE Materials(
  name VARCHAR(20) NOT NULL,
  location INT NOT NULL
);
```
```
CREATE TABLE RecipeSteps(
  stepNum INT NOT NULL,
  recipe VARCHAR(100) NOT NULL,
  foodID INT NOT NULL
);
```

## Install Nanum Fonts if you are using Korean
```
sudo apt update && sudo apt upgrade
```
```
sudo apt install fonts-nanum
```

## Set Environment Variables
Edit `~/.profile` with your editor and add the following

```
export OPENAI_API_KEY=Your_API_Key
export MYSQL_PASSWORD=Your_password
export DISPLAY=:0
```
Then run this command to apply changes
```
source ~/.profile
```

## Kivy Display Dependencies
Run Following commands to install dependencies to successfully run the program on your screen.
```
sudo apt-get install libsdl2-image-2.0-0
```
```
sudo apt-get install python3-xlib
```

## Mic settings
```
sudo apt install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev flac
```
```
pip install pyaudio requests websockets
```
Run the following commands to check your mic USB port and sound card number.
```
lsusb
```
```
arecord -l
```
```
cat /proc/asound/cards
```
```
cat /proc/asound/modules
```
Set the default card in the following file
```
sudo nano /usr/share/alsa/alsa.conf
```
For example if your card is 2
```
defaults.ctl.card 2
defaults.pcm.card 2
```
Save and reboot
```
sudo reboot
```
