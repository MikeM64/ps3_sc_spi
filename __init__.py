##
## Copyright (C) 2021 - MikeM64
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

'''
The PS3-SC-SPI protocol decoder builds on top of the SPI decoder to
display individual packets sent over the SPI bus between BE and SC.

In this particular instance, the master is always the SysCon and the
slave is always the Cell.
'''

from .pd import Decoder
