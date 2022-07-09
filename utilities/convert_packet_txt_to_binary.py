#!/usr/bin/env python3
import os
import sys

from argparse import ArgumentParser


def parse_args(argv):
    parser = ArgumentParser(
        description='Converts packet from textual from to a binary form.')
    parser.add_argument('packet', help='Path to a packet in textual form.')
    args = parser.parse_args(argv)
    return args


def read_packet_txt_from_path(packet_txt):
    print(f'Reading from: {packet_txt}')
    if not os.path.exists(packet_txt):
        raise ValueError(f'Invalid path {packet_txt}')
    with open(packet_txt, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        lines = [l for l in lines if l and not l.startswith('#')]
    assert len(lines) == 1, 'invalid multi-line file.'
    line = lines[0]
    assert len(line) > 0, len(line) % 2 == 0
    return line


def convert_txt_to_bytes(line):
    bytes_ = []
    for i in range(0, len(line), 2):
        bytes_.append(int(line[i:i + 2], 16))
    bytes_ = bytes(bytes_)
    return bytes_


def dump_to_file(dst, bytes_):
    print(f'Writing to: {dst}')
    with open(dst, 'wb') as f:
        f.write(bytes_)


def get_dst_from_src(packet_txt):
    file_, ext = os.path.splitext(packet_txt)
    file_ = file_.rstrip('/')
    dst = f'{file_}.bin'
    return dst


def convert_packet_txt_to_binary(packet_txt):
    line = read_packet_txt_from_path(packet_txt)
    bytes_ = convert_txt_to_bytes(line)
    dst = get_dst_from_src(packet_txt)
    dump_to_file(dst, bytes_)
    return dst


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    convert_packet_txt_to_binary(args.packet)
    print('Done')


if __name__ == '__main__':
    main()
