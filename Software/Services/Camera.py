import argparse
import logging
import os
from subprocess import Popen

logger = logging.getLogger('CatFeeder')


def StartRecording(config):
    filename = GetVideoName(config)
    return _execute(f'raspivid --timeout {config.VideoDuration}000 --mode 4 --nopreview --output {filename}.h264')

def StartEncoding(config):
    filename = GetVideoName(config)
    return _execute(f'ffmpeg -hide_banner -loglevel error -i {filename}.h264 {filename}.mp4 -y')

def StartExtracting(config):
    filename = GetVideoName(config)
    return _execute(f'ffmpeg -hide_banner -loglevel error -ss {config.PosterDelay} -i {filename}.mp4 -vframes 1 -vf "scale=640:480" {filename}.jpg -y')

def GetVideoName(config): return os.path.join(config.VideoLocation, config.VideoName)

def _execute(command):
    logger.info(f'Executing "{command}"...')
    p = Popen(command, shell=True)
    return p

if __name__ == '__main__':
    import Config

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')

    logger.setLevel(logging.INFO)

    if StartRecording(Config).wait() != 0:
        print('Video recording failed')
        exit()

    if StartEncoding(Config).wait() != 0:
        print('Video encoding failed')
        exit()

    if StartExtracting(Config).wait() != 0:
        print('Poster extracting failed')
        exit()
