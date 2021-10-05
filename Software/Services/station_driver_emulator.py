import json
import asyncio

import time
import signal
import sys
import random

from azure.iot.device import Message
from device_exception import DeviceException

class StationDriver:
    def __init__(self, device, loop):
        self.Device = device
        self.Loop = loop
        self.Delay = 5
        self.Tasks = asyncio.gather(self.send_telemetry())

        print('emulator ready')


    async def send_telemetry(self):
        print(f'Sending telemetry from the provisioned device every {self.Delay} seconds')
        while True:
            payload = {
                'Status': 'emulating'
            }

            msg = Message(json.dumps(payload))
            await self.Device.send_message(msg, )
            print(f'Sent message: {msg}')
            await asyncio.sleep(self.Delay)


    def reboot(self):
        print('emulate rebooting')


    def shutdown(self):
        print('emulate shutdown')


    def take_photo(self):
        print(f'emulate take photo')


    async def take_video(self, seconds):
        print(f'emulate take_video({seconds})')
        await asyncio.sleep(seconds)
        print(f'take_video completed')


    def run_food_cycle(self, scoops):
        print(f'emulate run_food_cycle({scoops})')
        time.sleep(5)
        print(f'run_food_cycle completed')


    def stop(self):
        self.Tasks.add_done_callback(lambda r: r.exception())
        self.Tasks.cancel()
        self.Tasks = None
        print(f'emulate stop()')
