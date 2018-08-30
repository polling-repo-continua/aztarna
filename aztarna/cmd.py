#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from argparse import ArgumentParser
from aztarna.sros import SROSScanner
from aztarna.ros import ROSScanner


def main():
    logger = logging.getLogger(__name__)
    parser = ArgumentParser(description='Aztarna')
    parser.add_argument('-t', '--type', help='<ROS/SROS> Scan ROS or SROS hosts', required=True)
    parser.add_argument('-a', '--address', help='Single address or network range to scan.')
    parser.add_argument('-p', '--ports', help='Port or Port range to scan', required=True)
    parser.add_argument('-i', '--input_file', help='Input file of addresses to use for scanning')
    parser.add_argument('-o', '--out_file', help='Output file for the results')
    parser.add_argument('-e', '--extended', help='Extended scan of the hosts')
    args = parser.parse_args()
    try:
        if args.type == 'ROS':
            scanner = ROSScanner()
        elif args.type == 'SROS':
            scanner = SROSScanner()
        else:
            logger.critical('Invalid type selected')
            return

        if args.input_file:
            scanner.load_from_file(args.input_file)
        else:
            if args.address:
                scanner.net_range = args.address
            else:
                logger.critical('No file or addresses defined')
                return

        scanner.ports = range(int(args.ports.split('-')[0]), int(args.ports.split('-')[1]))
        scanner.extended = args.extended
        scanner.scan()

        if args.out_file:
            scanner.write_to_file(args.out_file)
        else:
            scanner.print_results()
    except Exception as e:
        logger.critical('Exception occurred during execution')
        raise e


if __name__ == '__main__':
    main()