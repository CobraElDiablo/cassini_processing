#!/usr/bin/env python

import sys
import argparse

from isis3 import utils
import isis3.importexport as importexport

if __name__ == "__main__":

    try:
        utils.is_isis3_initialized()
    except:
        print "ISIS3 has not been initialized. Please do so. Now."
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="Source cube file", required=True, type=str, nargs='+')

    args = parser.parse_args()

    source = args.data

    for file_name in source:
        if file_name[-3:].upper() != "CUB":
            print "Not a ISIS cube file file. Skipping '%s'"%file_name
        else:
            out_file_tiff = utils.output_tiff_from_label(file_name)
            importexport.isis2std_grayscale(file_name, out_file_tiff, minimum=None, maximum=None)
