##
## Copyright (C) 2011 Gareth McMullin <gareth@blacksphere.co.nz>
## Copyright (C) 2012-2014 Uwe Hermann <uwe@hermann-uwe.de>
## Copyright (C) 2019 DreamSourceLab <support@dreamsourcelab.com>
## Copyright (C) MikeM64
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

import sigrokdecode as srd
from collections import namedtuple

Data = namedtuple('Data', ['ss', 'es', 'val'])

# From the CELL HIG, page 101
cell_be_chip_id = [
    "Serial SPI Memory",
    "Cell BE Processor",
    "IOIF0 Device",
    "IOIF1 Device",
    "System Controller",
    "Reserved 5",
    "Reserved 6",
    "Reserved 7",
    "Reserved 8",
    "Reserved 9",
    "Reserved xA",
    "Reserved xB",
    "Reserved xC",
    "Reserved xD",
    "Reserved xE",
    "Reserved xF",
]

multichip_id = [
    "Cell BE 0",
    "Cell BE 1",
    "Cell BE 2",
    "Cell BE 3",
]

command_id = [
    "Read",
    "Write",
    "Reserved 2",
    "Reserved 3",
]


class Decoder(srd.Decoder):
    api_version = 3
    id = 'ps3_sc_spi'
    name = 'PS3: SC SPI'
    longname = 'PS3 SysCon Serial Peripheral Interface Decoder'
    desc = 'Full-duplex, synchronous, serial bus.'
    license = 'gplv2+'
    inputs = ['spi']
    outputs = []
    tags = ['Embedded/ps3']
    annotations = (
        ('be-sc-command', 'BE -> SC: SPI Command'),
        ('be-sc-address', 'BE -> SC: SPI Address'),
        ('be-sc-data', 'BE -> SC: Data'),
        ('sc-be-command', 'SC -> BE: SPI Command'),
        ('sc-be-address', 'SC -> BE: SPI Address'),
        ('sc-be-data', 'SC -> BE: Data'),
    )
    annotation_rows = (
        ('besc-cmd', 'BE to SC Command', (0, )),
        ('besc-addr', 'BE to SC Address', (1, )),
        ('besc-data', 'BE to SC Data', (2, )),
        ('scbe-cmd', 'SC to BE Command', (3, )),
        ('scbe-addr', 'SC to BE Address', (4, )),
        ('scbe-data', 'SC to BE Data', (5, )),
    )
    options = ()

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def annotate_be_sc_packet(self, data):
        startsample = data[0].ss
        endsample = data[-1].es

        self.put(startsample, endsample, self.out_ann,
            [0, [command_id[data[0].val & 0x3] + " " +
               multichip_id[(data[0].val & 0xc) >> 2] + " " +
               cell_be_chip_id[(data[0].val & 0xF0) >> 4]]])
        self.put(startsample, endsample, self.out_ann,
            [1, [hex(data[1].val << 8 | data[2].val)]])
        self.put(startsample, endsample, self.out_ann,
            [2, [' '.join(hex(byte.val) for byte in data[3:])]])

    def annotate_sc_be_packet(self, data):
        startsample = data[0].ss
        endsample = data[-1].es

        self.put(startsample, endsample, self.out_ann,
            [3, [command_id[data[0].val & 0x3] + " " +
               multichip_id[(data[0].val & 0xc) >> 2] + " " +
               cell_be_chip_id[(data[0].val & 0xF0) >> 4]]])
        self.put(startsample, endsample, self.out_ann,
            [4, [hex(data[1].val << 8 | data[2].val)]])
        self.put(startsample, endsample, self.out_ann,
            [5, [' '.join(hex(byte.val) for byte in data[3:])]])

    def decode(self, ss, es, data):
        pkt_type, mosi_data, miso_data = data
        # Only decode SPI block transfers for now
        if pkt_type == "TRANSFER":
            # Minimum SPI transfer size is 3 for PS3
            if len(miso_data) >= 3:
                self.annotate_be_sc_packet(miso_data)
            if len(mosi_data) >= 3:
                self.annotate_sc_be_packet(mosi_data)
