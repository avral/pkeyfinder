"""
Bitcoin private/public key and seed finder.

@author: https://avral.pro
"""
import re
import os
import sys
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description=(
    'Bitcoin seed/private/public keys finder.'
    ' Provide path or use pipe.'
))

parser.add_argument('path', type=str, help="path name", default=None)
parser.add_argument('-a', '--addresses', action="store_true", help="search addresses")
parser.add_argument('-s', '--seeds', action="store_true", help="search addresses")
parser.add_argument('-sl', type=int, default=12, help="defines the seed length")
parser.add_argument('-r', action="store_true", help="recursivelly")

args = parser.parse_args()

CONTENT = ''
SEED_RGEX = ' '.join(['[a-z]+'] * args.sl)
PKEY_RGEX = '.*([5KL][1-9A-HJ-NP-Za-km-z]{50,51}).*'
ADDRESS_RGEX = '.*([13][a-km-zA-HJ-NP-Z1-9]{25,34}).*'


def parse(CONTENT):
    print('\033[94mLooking for pkeys... \033[0m')
    pkeys = re.findall(PKEY_RGEX, CONTENT, re.MULTILINE)

    for pkey in pkeys:
        print(f'\033[93m Found pkey in {args.path}: {pkey[:5]}... \033[0m')

    if args.addresses:
        print('\033[94mLooking for addresses... \033[0m')
        addresses = re.findall(ADDRESS_RGEX, CONTENT, re.MULTILINE)

        for addr in addresses:
            print(f'\033[93m Found address in {args.path}: {addr} \033[0m')

    if args.seeds:
        print('\033[94mLooking for seed phrases... \033[0m')
        seeds = re.findall(SEED_RGEX, CONTENT, re.MULTILINE)

        for seed in seeds:
            print(f'\033[93m Found seed in {args.path}: "{seed[:20]}..." \033[0m')


if args.path:
    if args.r:
        for r, d, f in os.walk(args.path):
            for file in f:
                print(f'\033[94mScan\033[0m {os.path.join(r, file)} ... ')
                CONTENT = Path(os.path.join(r, file)).read_text()
                parse(CONTENT)
    else:
        try:
            CONTENT = Path(args.path).read_text()
        except FileNotFoundError as e:
            print(e)
            exit()

        parse(CONTENT)

else:
    if sys.stdin.isatty():
        raise Exception('stdin is empty: provide path or use pipe')

    CONTENT = ''.join(sys.stdin).rstrip()
    parse(CONTENT)
