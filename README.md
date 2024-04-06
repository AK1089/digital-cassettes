# Avish's Digital Cassettes

## Description

This is a Raspberry Pi project designed to bridge the physical and digital worlds using NFC technology. I grew up listening to music in the post-vinyl & post-cassette era, and while I love the convenience, data tracking, and general digital nature of Spotify, I do like the idea of tactile interaction when interacting with music. With this project, I made scale 3D-printed models of cassettes, adorned with custom stickers designed to replicate cassette labels, and added a slot for a unique NFC tag inside each. An NFC reader connected to the Pi reads the tag when it's presented and uses the Spotipy Python API to play the music on my Spotify account.

## Features

   - **Persistence Across Restarts**: Tag data and actions are saved and restored across system restarts.
   - **Graceful Shutdowns**: Designed to handle shutdowns and restarts safely.
   - **Automatic Music Binding**: New NFC tags are instantly paired to the album/playlist of your choice when presented for the first time.
   - **Fast Response**: Music starts playing within two seconds of presenting the tag to the reader.

## Hardware Requirements

   - Raspberry Pi (Tested on [Raspberry Pi Zero](https://thepihut.com/products/raspberry-pi-zero-wh-with-pre-soldered-header?variant=547332849681&currency=GBP&utm_medium=product_sync))
   - NFC Reader (Tested with [RC522](https://uk.robotshop.com/products/mifare-rc522-module-rfid-reader))
   - NFC Tags (Tested with [NTAG215](https://www.amazon.co.uk/dp/B0CKLCYSW1?psc=1&ref=ppx_yo2ov_dt_b_product_details))
   - WiFi Connection

## Software Requirements

- See `requirements.txt`

## Installation

1. **Import the Code**:
   The repository contains several other large files which aren't needed on the Pi, so I would recommend against cloning it directly. Instead, simply copy `fetch.py` `fetch.sh`, and `script.py` into a directory. Also create blank files `restart_log.txt` and `tag_data.json`.

2. **Install Dependencies**:
   ```
   pip3 install -r requirements.txt
   ```

3. **Raspberry Pi Hardware Setup**:
   Wire your NFC reader to the Raspberry Pi using the SPI wiring protocol.
- VCC to 3.3V on Pi
- RST to GPIO25
- GND to Ground on Pi
- MISO to GPIO9 (MISO)
- MOSI to GPIO10 (MOSI)
- SCK to GPIO11 (SCLK)
- SDA to GPIO8 (CE0)
  
   Note that on the Pi, all these connections should be adjacent in a block.

4. **Deploy the Systemd Service**:

   Create a service file with `sudo nano /etc/systemd/system/fetch.service`, and add the lines
   ```
   [Unit]
   Description=Cassette Project Service
   After=network-online.target
   Wants=network-online.target
   
   [Service]
   Type=simple
   ExecStart=/bin/bash .../fetch.sh
   User=pi
   WorkingDirectory=...
   Restart=always
   Environment="DISCORD_BOT_TOKEN=..."
   Environment="SPOTIPY_CLIENT_ID=..."
   Environment="SPOTIPY_CLIENT_SECRET=..."
   Environment="SPOTIPY_REFRESH_TOKEN=..."
  
  
   [Install]
   WantedBy=multi-user.target
   
   ```
   with the `...`s being the path to the bash script, the directory of the project, and your authentication details respectively. Then run
   ```
   sudo systemctl daemon-reload
   sudo systemctl enable --now fetch.service
   ```
   to enable your service.

5. **Create the Cassettes**:
   Print the `cassette.gcode` file on any compatible 3D printer (I use an AnyCubic i3 Mega). Insert your NFC tag into the slot at the top of the cassette.

   Create your stickers based on the album or playlist of your choice by editing the template. I've included a couple examples from [my favourite band](https://open.spotify.com/artist/4yvcSjfu4PC0CYQyLy4wSq) at the top of the file. I made these with Apple's Pages software, but if you can't use that then just edit the PDF directly.

   Print out the stickers on A4 sticker paper, and cut them out with scissors or a box cutter. Cut out the black part in the centre of the sticker, and cut the rectangular "tape window" from it. Stick the main label in the appropriately shaped indent, and the tape window in the indent in the very middle (between the two holes).

## Usage

1. **Running the Project**:
   The project runs automatically on boot via the `fetch.service`. Manual interaction can be done through SSH or directly on the Raspberry Pi.

2. **Saving New NFC Tags**:
   While playing an album or playlist on Spotify, tap a previously unused tag/cassette on the reader. It will automatically pair the tag to that album/playlist, and this persists across restarts.

3. **Playing Music**:
   When you have a tag/cassette paired already, tap it against the reader to automatically start the playlist or album it is bound to from the beginning. Happy listening!
