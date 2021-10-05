import argparse
import logging
import os
from subprocess import Popen

logger = logging.getLogger('CatFeeder')


def StartRecording(config, seconds):
    filename = GetVideoName(config)
    return _execute(f'raspivid --timeout {seconds * 1000} --mode 4 --nopreview --output {filename}.h264')

def TakePhoto(filename):
    os.system(f'raspistill --mode 4 --nopreview --output {filename}')

def TakeVideo(name, seconds):
    os.system(f'raspivid --timeout {seconds * 1000} --mode 4 --nopreview --output {name}.h264')
    outputFilename = f'{name}.mp4'
    os.system(f'ffmpeg -hide_banner -loglevel error -i {name}.h264 {outputFilename} -y')
    return outputFilename

def StartEncoding(config):
    filename = GetVideoName(config)
    return _execute(f'ffmpeg -hide_banner -loglevel error -i {filename}.h264 {filename}.mp4 -y')

def StartExtracting(config, delay):
    filename = GetVideoName(config)
    return _execute(f'ffmpeg -hide_banner -loglevel error -ss {delay} -i {filename}.mp4 -vframes 1 -vf "scale=640:480" {filename}.jpg -y')

def GetVideoName(config): return os.path.join(config.VideoLocation, config.VideoName)

def _execute(command):
    logger.info(f'Executing "{command}"...')
    p = Popen(command, shell=True)
    return p

if __name__ == '__main__':
    import Config

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')

    logger.setLevel(logging.INFO)

    if StartRecording(Config, 2).wait() != 0:
        print('Video recording failed')
        exit()

    if StartEncoding(Config).wait() != 0:
        print('Video encoding failed')
        exit()

    if StartExtracting(Config, 1).wait() != 0:
        print('Poster extracting failed')
        exit()
