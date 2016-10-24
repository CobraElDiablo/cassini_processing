#!/usr/bin/python
import os
import sys
import re
import subprocess
import datetime
import glob
import argparse

from isis3 import utils

def print_if_verbose(s, is_verbose=True):
    if is_verbose:
        print s

def process_data_file(lbl_file_name, is_ringplane, require_target, require_filters, metadata_only, is_verbose):
    source = utils.guess_from_filename_prefix(lbl_file_name)
    source_dirname = os.path.dirname(source)
    if source_dirname == "":
        source_dirname = "."

    if not os.path.exists(source):
        print "File %s does not exist"%source
    else:
        print_if_verbose("Processing %s"%source, is_verbose)

    target = utils.get_target(source)
    print_if_verbose("Target: %s"%target, is_verbose)

    product_id = utils.get_product_id(source)
    print_if_verbose("Product ID: %s"%product_id, is_verbose)

    print_if_verbose("Ringplace Shape: %s"%("Yes" if is_ringplane else "No"), is_verbose)

    filter1, filter2 = utils.get_filters(source)
    print_if_verbose("Filter #1: %s"%filter1, is_verbose)
    print_if_verbose("Filter #2: %s"%filter2, is_verbose)

    lines = utils.get_num_lines(source)
    print_if_verbose("Lines: %s"%lines, is_verbose)

    line_samples = utils.get_num_line_samples(source)
    print_if_verbose("Samples per line: %s"%line_samples, is_verbose)

    sample_bits = utils.get_sample_bits(source)
    print_if_verbose("Bits per sample: %s"%sample_bits, is_verbose)

    image_date = utils.get_image_time(source)
    print_if_verbose("Image Date: %s"%image_date, is_verbose)

    out_file_base = utils.output_filename_from_label(source)

    out_file_tiff = "%s.tif"%out_file_base
    print_if_verbose("Output Tiff: %s"%out_file_tiff, is_verbose)

    out_file_cub = "%s.cub"%out_file_base
    print_if_verbose("Output Cube: %s"%out_file_cub, is_verbose)

    if metadata_only:
        return

    if skip_existing and os.path.exists(out_file_cub) and os.path.exists(out_file_tiff):
        print "Output exists, skipping."
        return

    if require_target is not None and not require_target.upper() == target.upper():
        print "Target mismatch, exiting."
        return

    if require_filters is not None and not (filter1 in require_filters or filter2 in require_filters):
        print "Filter mismatch, exiting."
        return

    utils.process_pds_data_file(source, is_ringplane=is_ringplane, is_verbose=is_verbose)


if __name__ == "__main__":

    try:
        utils.is_isis3_initialized()
    except:
        print "ISIS3 has not been initialized. Please do so. Now."
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="Source PDS dataset", required=True, type=str, nargs='+')
    parser.add_argument("-r", "--ringplane", help="Input data is of a ring plane", action="store_true")
    parser.add_argument("-m", "--metadata", help="Print metadata and exit", action="store_true")
    parser.add_argument("-f", "--filter", help="Require filter or exit", required=False, type=str, nargs='+')
    parser.add_argument("-t", "--target", help="Require target or exit", required=False, type=str)
    parser.add_argument("-s", "--skipexisting", help="Skip processing if output already exists", action="store_true")
    parser.add_argument("-v", "--verbose", help="Verbose output (includes ISIS3 command output)", action="store_true")
    args = parser.parse_args()

    source = args.data

    is_ringplane = args.ringplane
    metadata_only = args.metadata

    require_filters = args.filter
    require_target = args.target

    skip_existing = args.skipexisting

    is_verbose = args.verbose

    for lbl_file_name in source:
        if lbl_file_name[-3:].upper() != "LBL":
            print "Not a PDS label file. Skipping '%s'"%lbl_file_name
        else:
            process_data_file(lbl_file_name, is_ringplane, require_target, require_filters, metadata_only, is_verbose)

    print_if_verbose("Done", is_verbose)
