import logging


def convert_size(in_bytes):
    mb = in_bytes / 1048576.0
    kb = in_bytes / 1024.0
    gb = in_bytes / 1073741824.0

    if kb <= 612.0:
        d = "{} kB".format(int(kb))
    elif gb >= 1.0:
        d = "{} GB".format(int(gb))
    else:
        d = "{} MB".format(int(mb))
    return d


def check_file_type(types, ext):
    try:
        for k, v in iter(types.items()):
            # solves bug where some file extensions are uppercase
            if ext.lower() in v:
                d = k
                return str(d)

    except Exception as e:
        logging.error("Unable to locate fileType from the supplied variables")
        print(e)