import asyncio
import json
import logging
import os
from datetime import datetime

from azure.iot.device import Message

import Config
import Light
from BlobUpload import UploadPackage
from Camera import TakePhoto, TakeVideo
from FoodCycle import FullCycle
from FoodDispenser import TrunkDown

# from device_exception import DeviceException

logger = logging.getLogger('CatFeeder')


class StationDriver:
    def __init__(self, device, loop):
        self.Device = device
        self.Loop = loop
        self.Delay = 60
        self.Tasks = asyncio.gather(self.send_telemetry())
        TrunkDown(Config.TrunkMovementTime)

        logger.info(f'Device started.')


    async def send_telemetry(self):
        logger.debug(f'Sending telemetry from the provisioned device every {self.Delay} seconds')
        while True:
            payload = {
                'Status': 'listening'
            }

            msg = Message(json.dumps(payload))
            await self.Device.send_message(msg)
            logger.debug(f'Sent message: {msg}')
            await asyncio.sleep(self.Delay)


    def reboot(self):
        logger.info('rebooting')
        os.system('sudo reboot')


    def take_photo(self):
        filename = os.path.join(Config.VideoLocation, 'photo.jpg')
        now = datetime.now(datetime.utcnow().astimezone().tzinfo)
        try:
            Light.On()
            TakePhoto(filename)
        finally:
            Light.Off()
        logger.debug(f'photo taken {filename}')
        UploadPackage(filename, now, Config)


    async def take_video(self, seconds):
        logger.info(f'take_video({seconds})')

        if seconds > 60 * 5:
            seconds = 60 * 5

        config = Config
        now = datetime.now(datetime.utcnow().astimezone().tzinfo)

        try:
            Light.On()

            name = os.path.join(config.VideoLocation, 'video')
            filename = TakeVideo(name, seconds)

            Light.Off() # todo: light stays on too long, including encoding time

            UploadPackage(filename, now, config)

            logger.info(f'take_video completed')
        finally:
            Light.Off()


    def run_food_cycle(self, scoops):
        logger.info(f'run_food_cycle({scoops})')
        FullCycle(Config, scoops)
        logger.info(f'run_food_cycle completed')
