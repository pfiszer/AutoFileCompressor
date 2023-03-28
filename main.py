import gzip
import pathlib
import os
import logging
import time

CONFIG = {"compressionLevel": 5, "rootFolderPath": ".",
          "filePattern": ["*.csv"], "loggingLevel": logging.INFO, "timeInterval": 10}


def compressAndDelete(filename):
    with open(filename, "rb") as f_in, gzip.open(f"{filename}.gz", "wb") as f_out:
        data = f_in.read()
        f_out.write(gzip.compress(data, CONFIG["compressionLevel"]))
    os.remove(filename)


if __name__ == "__main__":
    # Open Config file
    try:
        with open("settings.cfg", "r") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("#"):
                continue
            else:
                key, val = line.split("=")
                match key:
                    case "compressionLevel":
                        try:
                            val = int(val)
                            val = abs(val) if abs(val) <= 9 else None
                        except:
                            print("Invalid compression level")

    except:
        with open("settings.cfg", "w") as f:
            pass
    logging.basicConfig(filename=f'app_{time.strftime("%Y%m%d%H%M%S")}.log', filemode='w',
                        level=CONFIG["loggingLevel"], format='[%(asctime)s]: {%(levelname)s} %(message)s')
    while True:
        noFiles = 0
        for pattern in CONFIG["filePattern"]:
            try:
                folder = pathlib.Path(
                    CONFIG["rootFolderPath"]).glob(f"**/{pattern}")
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
                        logging.critical(f"New exception: {e}", exc_info=True)
            finally:
                logging.debug(f"Compression for pattern {pattern} complete.")
        logging.info(f"Compressed {noFiles} files.")
        print(f"Compressed {noFiles} files.")
        time.sleep(CONFIG["timeInterval"])
