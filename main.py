import gzip
import pathlib
import os


def compressAndDelete(filename):
    with open(filename, "rb") as f_in, gzip.open(f"{filename}.gz", "wb") as f_out:
        data = f_in.read()
        f_out.write(gzip.compress(data, 9))
    os.remove(filename)


for f in pathlib.Path(".").glob("**/*.csv"):
    print(f)
    compressAndDelete(f)
