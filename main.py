import configparser
import gzip
import pathlib
import os
import logging
import time
from math import inf as infinity

config = configparser.ConfigParser()
config["app"] = {"compressionLevel": 5, "loggingLevel": logging.INFO,
                 "timeInterval": 60, "iterations": infinity}
config["filePatterns"] = {}
config["folderPaths"] = {}

if config.read('settings.ini') == []:
    with open('settings.ini', "w") as f:
        config.write(f)


def compressAndDelete(filename):
    with open(filename, "rb") as f_in, gzip.open(f"{filename}.gz", "wb", compresslevel=config["app"]["compressionLevel"]) as f_out:
        f_out.write(f_in.read())
    os.remove(filename)


if __name__ == "__main__":

    # Open Config file
    if not os.path.exists("./logs"):
        os.mkdir("./logs")
    logging.basicConfig(filename=f'./logs/app_{time.strftime("%Y%m%d%H%M%S")}.log', filemode='w',
                        level=config.getint("app", "loggingLevel", fallback=logging.INFO), format='[%(asctime)s]: {%(levelname)s} %(message)s')
    iteration = 0
    while iteration < config.getfloat("app", "iterations", fallback=infinity):
        startTime = time.time()
        noFiles = 0
        for pattern in config["filePatterns"].keys():
            for path in config["folderPaths"].keys():
                try:
                    folder = pathlib.Path(path).glob(f"**/{pattern}")
                except:
                    logging.error(
                        f"{pattern} is not a valid pattern", exc_info=True)
                else:
                    for f in folder:
                        logging.debug(f"{f} is processed.")
                        try:
                            compressAndDelete(f)
                            noFiles += 1
                        except Exception as e:
                            logging.critical(
                                f"New exception: {e}", exc_info=True)
                finally:
                    logging.debug(
                        f"Compression for pattern {pattern} complete.")
        logging.info(f"Compressed {noFiles} files.")
        print(f"Compressed {noFiles} files.")
        while time.time()-startTime < config.getint("app", "timeInterval"):
            pass
        if config.getint("app", "iterations", fallback=False):
            iteration += 1
