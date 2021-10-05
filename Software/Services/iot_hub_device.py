import asyncio
import logging
import sys
import datetime
import socket

from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse
from opencensus.ext.azure.log_exporter import AzureLogHandler, AzureEventHandler

from device_exception import DeviceException
import Config

logger = logging.getLogger('CatFeeder')

async def main(emulator):
    sys.path.append('..')
    if emulator:
        from station_driver_emulator import StationDriver
        from emulator_credentials import SCOPE_ID, DEVICE_ID, SYMMETRIC_KEY
    else:
        from station_driver import StationDriver
        from credentials import SCOPE_ID, DEVICE_ID, SYMMETRIC_KEY

    provisioning_host = 'global.azure-devices-provisioning.net'

    async def wait_for_connection():
        for _ in range(0, 20):
          try:
            socket.gethostbyname(provisioning_host)
            return True
          except:
            await asyncio.sleep(1)
        return False

    async def register_device():
        provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host=provisioning_host,
            registration_id=DEVICE_ID,
            id_scope=SCOPE_ID,
            symmetric_key=SYMMETRIC_KEY)

        registration_result = await provisioning_device_client.register()

        logger.info(f'Device registration result: {registration_result.status}')

        return registration_result

    async def get_device_client():
        if not await wait_for_connection():
            logger.error('IoT network not available.')
            return None

        device_client = None
        try:
            registration_result = await register_device()
            if registration_result.status == 'assigned':
                device_client = IoTHubDeviceClient.create_from_symmetric_key(
                    symmetric_key=SYMMETRIC_KEY,
                    hostname=registration_result.registration_state.assigned_hub,
                    device_id=registration_result.registration_state.device_id)
        finally:
            return device_client

    async def take_photo_command(request):
        station_driver.take_photo()
        response = MethodResponse.create_from_method_request(request, status = 200, payload='ok')
        await device_client.send_method_response(response)
        logger.debug('take_photo response sent')

    async def take_video_command(request):
        await device_client.send_method_response(MethodResponse.create_from_method_request(request, status = 202, payload='started'))
        await station_driver.take_video(float(request.payload))
        await device_client.patch_twin_reported_properties({ 'TakeVideo': { 'value': f'Completed at {datetime.datetime.today()}.' } })

    async def reboot_command(request):
        logger.info('Starting asynchronous reboot_command...')
        response = MethodResponse.create_from_method_request(request, status = 202, payload='rebooting')
        await device_client.send_method_response(response)
        logger.info('reboot response sent')
        station_driver.reboot()

    async def shutdown_command(request):
        await device_client.send_method_response(MethodResponse.create_from_method_request(request, status = 501, payload='Shutdown is not supported.'))
        # station_driver.shutdown()

    async def run_food_cycle_command(request):
        await device_client.send_method_response(MethodResponse.create_from_method_request(request, status = 202, payload='started'))
        station_driver.run_food_cycle(int(request.payload))
        await device_client.patch_twin_reported_properties({ 'RunFoodCycle': { 'value': f'Completed at {datetime.datetime.today()}.' } })

    commands = {
        'TakePhoto': take_photo_command,
        'TakeVideo': take_video_command,
        'Reboot': reboot_command,
        'Shutdown': shutdown_command,
        'RunFoodCycle': run_food_cycle_command,
    }

    async def patch_twin_reported_properties(name, value):
        await device_client.patch_twin_reported_properties(
            {
                'state': True,
                name: value
            })

    async def method_handler(request):
        logger.debug(f'method request #{request.request_id} {request.name}: {request.payload}')
        if request.name not in commands:
            error_message = f'{request.name} not in commands'
            logger.error(error_message)
            response = MethodResponse.create_from_method_request(request, status = 400, payload=error_message)
            await device_client.send_method_response(response)
            return
        try:
            await commands[request.name](request)
        except DeviceException as e:
            response = MethodResponse.create_from_method_request(request, status = 400, payload=e.args[0])
            await device_client.send_method_response(response)

    def stdin_listener():
        while True:
            selection = input('Press Q to quit\n')
            if selection == 'Q' or selection == 'q':
                logger.info('Quitting...')
                break

    loop = asyncio.get_running_loop()

    device_client = await get_device_client()

    if device_client is None:
        logger.error('Could not register device')
        return

    station_driver = StationDriver(device_client, loop)

    # device_client.on_message_received = message_handler
    device_client.on_method_request_received = method_handler
    # device_client.on_twin_desired_properties_patch_received = properties_handler

    await device_client.connect()

    if not device_client.connected:
        logger.error(f'Device could not connect')
        return

    logger.info('Device connected successfully')

    await device_client.patch_twin_reported_properties(
        {
            'Reboot':
            {
                'value': f'Started at {datetime.datetime.today()}.'
            }
        })

    # twin = await device_client.get_twin()
    # if 'desired' in twin: await properties_handler(twin['desired'])

    if emulator:
        user_finished = loop.run_in_executor(None, stdin_listener)
        await user_finished
        station_driver.stop()
    else:
        while True:
            await asyncio.sleep(10)
    await device_client.disconnect()


if __name__ == '__main__':
    print(sys.argv)
    emulator = 'emulator' in sys.argv

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')

    if emulator:
        logger.setLevel(logging.DEBUG)
    else:
        logger.addHandler(AzureLogHandler(connection_string=Config.AppInsightsConnectionString))
        logger.setLevel(logging.INFO)


    asyncio.run(main(emulator=emulator))