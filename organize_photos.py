import shutil
import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS

MONTH_FORMAT = {1: "01 January",
                2: "02 February",
                3: "03 March",
                4: "04 April",
                5: "05 May",
                6: "06 June",
                7: "07 July",
                8: "08 August",
                9: "09 September",
                10: "10 October",
                11: "11 November",
                12: "12 December"}


def get_exif_data(fname):
    ret = {}
    try:
        img = Image.open(fname)
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo is not None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        print 'IOERROR ' + fname
    return ret


def get_date_taken(file_path):
    exif_data = get_exif_data(file_path)
    if not 'DateTimeDigitized' in exif_data:
        return None, None, None
    dateTaken = exif_data['DateTimeDigitized']
    year = int(dateTaken[0:4])
    month = int(dateTaken[5:7])
    day = int(dateTaken[8:10])
    return year, month, day


def _is_jpeg(filename):
    lower = filename.lower()
    return lower.endswith(".jpg") or lower.endswith("jpeg")

SOURCE_DIRECTORY = "."
DESTINATION_DIRECTORY = "../Sorted_Pictures"


def traverse_target_directory():
    for root, dirs, files in os.walk(SOURCE_DIRECTORY):
        for name in files:
            if not _is_jpeg(name):
                continue
            full_path = "/".join((root, name))
            year, month, day = get_date_taken(full_path)
            if year is None:
                new_directory = "No_Meta_Data"
            else:
                new_directory = "%s - %s - %s" % (year, MONTH_FORMAT.get(month), day)

            target_directory = "/".join((DESTINATION_DIRECTORY, new_directory))
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            destination_path = "/".join((target_directory, name))
            print "Moving %s to %s..." % (full_path, destination_path)
            shutil.copy2(full_path, destination_path)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        SOURCE_DIRECTORY = sys.argv[1]
    if len(sys.argv) >= 3:
        DESTINATION_DIRECTORY = sys.argv[2]
    traverse_target_directory()
