#!/usr/bin/env python
# Copyright (c) 2012-2014 Erik Johansson <erik@ejohansson.se>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import tellcore.telldus as td


def raw_event(data, controller_id, cid):
    string = "[RAW] {0} <- {1}".format(controller_id, data)
    print(string)

import asyncio
loop = asyncio.get_event_loop()
dispatcher = td.AsyncioCallbackDispatcher(loop)

core = td.TelldusCore(callback_dispatcher=dispatcher)
callbacks = []
callbacks.append(core.register_raw_device_event(raw_event))

loop.run_forever()
