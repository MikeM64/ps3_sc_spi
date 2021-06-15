# ps3_sc_spi
Quick and dirty SPI decoder for DSView.

![Screenshot](https://github.com/mikem64/ps3_sc_spi/raw/master/images/Screenshot.png)

# Requirements
- DSView 1.12 (SigRok currently untested)
- The "1:SPI" decoder is used to initially decode the SPI stream. Make sure the frame decoder is turned ON.

# Installation
- Copy/clone this entire directory to your `decoders` directory
- Open your SPI trace in DSView
- Modify the settings of the "1:SPI" decoder instance to add "PS3: SC SPI" as a stacked decoder
