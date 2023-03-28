import gzip
import pathlib
import os
import logging
import time
from math import inf as infinity

CONFIG = {"compressionLevel": 5, "rootFolderPath": ".", "filePatterns": [
    "*.csv"], "loggingLevel": logging.INFO, "timeInterval": 60, "noIterations": infinity}


def compressAndDelete(filename):
    with open(filename, "rb") as f_in, gzip.open(f"{filename}.gz", "wb", compresslevel=CONFIG["compressionLevel"]) as f_out:
        f_out.write(f_in.read())
    os.remove(filename)


if __name__ == "__main__":
    # Open Config file
    try:
        with open("./settings.cfg", "r") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("#") or line == "\n":
                continue
            else:
                key, val = line.split("=")
                val = val.strip()
                match key:
                    case "compressionLevel":
                        try:
                            val = int(val)
                            val = abs(val) if abs(val) <= 9 else None
                        except:
                            val = None
                            print("Invalid compression level")
                    case "loggingLevel":
                        match val:
                            case "DEBUG":
                                val = logging.DEBUG
                            case "INFO":
                                val = logging.INFO
                            case "WARNING":
                                val = logging.WARNING
                            case "ERROR":
                                val = logging.ERROR
                            case "CRITICAL":
                                val = logging.CRITICAL
                            case _:
                                val = logging.INFO
                    case "timeInterval":
                        try:
                            val = float(val)
                            val = abs(val)
                        except:
                            val = None
                            print("Invalid time interval")
                    case "filePatterns":
                        val = val.split("|")
                        val = list(map(lambda x: x.strip(), val))
                    case "rootFolderPath":
                        val = val.split("|")
                        val = list(map(lambda x: x.strip(), val))
                    case "noIterations":
                        try:
                            val = int(val)
                            val = infinity if val < 0 else val
                        except:
                            val = None
                            print("Invalid compression level")

                CONFIG[key] = val if val != None else CONFIG[key]
        print("Config loaded.")
    except:
        with open("settings.cfg", "w") as f:
            f.write("""## To change the settings from default, enter config keys with values or uncomment following lines

## Compression level is an integer between 0 and 9, higher the compression level, smaller the file, but it takes longer to compress.
#compressionLevel=5

## Root folder is the folder the program will start searching for the files in, it will search all folders and subfolders in order to find matching files.
#rootFolderPath=.

## File pattern is the pattern in the name the program will look for when searching for files, use the pipe "|" character to separate patterns
#filePatterns=*.csv

## Number of iterations, integer that sets the number of times the program scans for files. When set to 0 or lower, it will run indefinetly.
#noIterations=-1

## Time interval is the time between the start of each iteration of the search measured in seconds (you can include milliseconds by using the dot "." character).
## It is recommended to set it to 0 when the number of iterations is 1
#timeInterval=60

## Logging level is the level of onformation saved to the .log file. Acceptable options are: DEBUG | INFO | WARNING | ERROR | CRITICAL
#loggingLevel=INFO""")
            quit()

    logging.basicConfig(filename=f'app_{time.strftime("%Y%m%d%H%M%S")}.log', filemode='w',
                        level=CONFIG["loggingLevel"], format='[%(asctime)s]: {%(levelname)s} %(message)s')
    iteration = 0
    while iteration < CONFIG["noIterations"]:
        startTime = time.time()
        noFiles = 0
        for pattern in CONFIG["filePatterns"]:
            for path in CONFIG["rootFolderPath"]:
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
        while time.time()-startTime < CONFIG["timeInterval"]:
            pass
        if CONFIG["noIterations"] != infinity:
            iteration += 1
