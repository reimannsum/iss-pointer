# Raspberry Pi ISS Pointer

## 1.0.2
1. Adding models for a 3d printed pointer shaped like a telescope. 
- The base is to be turned by a motor [like this](https://www.ebay.com/sch/i.html?&_nkw=39MM+Thin+2-phase+4-wire+Stepper+Motor&_sacat=0)
- The arm will be turned by a motor [like this](https://www.ebay.com/sch/i.html?&_nkw=Micro+15MM+DC+5V+2-Phase+4-Wire+Metal+Gear+Stepper+Motor&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=39MM+Thin+2-phase+4-wire+Stepper+Motor)

## 1.0.1 (August 27, 2019)

1. Updated from PyEphem to skyfield (same author, same purpose, complete rebuild)
2. will add the ability to calculate the magnetic declination based on the location of the observer
3. will add support for a compass (magnometer) to allow the pointer to not need to be aligned north.


## 1.0.0 (December 12, 2018)

1. Updated for avalon framework 1.6.x.

## 0.2 alpha (Jan 16, 2018)

1. Added main controller
1. Fixed motor controller
1. Project Imported

## Description

The raspberry pi ISS Pointer is a simple device that will always point to the current location of the International Space Station (ISS).
This project is initialized as an ISU project.

## Demo

![Preview](https://img.youtube.com/vi/6hxp3M6DFm8/maxresdefault.jpg)

You can watch the demo video at [HERE](https://www.youtube.com/watch?v=6hxp3M6DFm8). If that link doesn't work, here's a manual one: https://www.youtube.com/watch?v=6hxp3M6DFm8

## Usages

First, you'll have to have hardware as shown in the image above, and then you'll have to connect controllers to the RPi GPIO headers. Different hardware will require different setups. Our configuration is shown below in the GPIO Header section.

After setting up the hardware, you can just clone and run the python script.

```bash
$ git clone https://github.com/K4YT3X/iss-pointer.git
$ cd iss-pointer/bin
$ sudo python3 isspointer.py
```

## Included model
![Telescope model](Telescope.jpeg)

## GPIO Header

![pi3_gpio](https://user-images.githubusercontent.com/21986859/34141154-78ec6628-e44d-11e7-8ef6-7ffcb87f79a1.png)
![isspinsetup](https://user-images.githubusercontent.com/21986859/35024318-d426e93e-fb0c-11e7-8e15-41f8bb0b7db9.png)

**It's important to note to always reset these pins back to the input mode to avoid
frying them.**
