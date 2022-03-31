#
# Runs check_file() in sicd_consistency.py on a single file or every file within
# a directory.
#
# To convert this tool into a single Windows executable, install the "pyinstaller"
# python package and run the following command:
#
# pyinstaller --console --onefile --add-data 
#   '<path to sarpy>/sarpy/io/complex/sicd_schema/*.xsd;sarpy/io/complex/sicd_schema' 
#   '<directory of validate_sicds.py>/validate_sicds.py'
#
# Executable is found in <directory of validate_sicds.py>/dist/validate_sicds.exe
#

import argparse
import logging
import os

from sarpy.consistency import sicd_consistency

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Validate SICD Products',description='Runs NGA validation on single SICD NITF or all SICD NITFs within input directory')
    parser.add_argument('input_path', help='Full path to input file or files directory')
    parser.add_argument(
        '-d', '--output_dir', default='', help='Full path to desired output directory. Default is directory of executable')
    parser.add_argument(
        '-o', '--output_log_name', default='', help='Name of output log file. Default is base name of input_path')
    config = parser.parse_args()

    if not config.output_dir:
        config.output_dir = os.getcwd()

    if not config.output_log_name:
        config.output_log_name = os.path.basename(config.input_path) + ".log"

    out_file = os.path.join(config.output_dir, config.output_log_name)

    logging.basicConfig(level='INFO', filename=out_file, filemode='w', format='%(levelname)s:%(filename)s:%(funcName)s:line %(lineno)d - %(message)s')
    logger = logging.getLogger()

    if '.' in config.input_path:
        valid = sicd_consistency.check_file(config.input_path)
        if valid:
            logger.info('SICD: {} has been validated with no significant findings\n'.format(config.input_path))
        else:
            logger.info('SICD: {} has apparent significant findings\n'.format(config.input_path))
    else:
        for subdir, dir, files in os.walk(config.input_path):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith('.ntf') or filepath.endswith('.nitf'):
                    valid = sicd_consistency.check_file(filepath)
                    if valid:
                        logger.info('SICD: {} has been validated with no significant findings\n'.format(filepath))
                    else:
                        logger.info('SICD: {} has apparent significant findings\n'.format(filepath))
