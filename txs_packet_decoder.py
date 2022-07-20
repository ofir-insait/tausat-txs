#!/usr/bin/env python3
import os
import sys
import struct

from argparse import ArgumentParser

from consts import TXS_PACKET_LEN

# Reed-solomon lookup table from ISIS.
LUT = {'00': '00', 'CC': '01', 'AC': '02', '60': '03', '79': '04', 'B5': '05', 'D5': '06', '19': '07', 'F0': '08', '3C': '09', '5C': '0A', '90': '0B', '89': '0C', '45': '0D', '25': '0E', 'E9': '0F', 'FD': '10', '31': '11', '51': '12', '9D': '13', '84': '14', '48': '15', '28': '16', 'E4': '17', '0D': '18', 'C1': '19', 'A1': '1A', '6D': '1B', '74': '1C', 'B8': '1D', 'D8': '1E', '14': '1F', '2E': '20', 'E2': '21', '82': '22', '4E': '23', '57': '24', '9B': '25', 'FB': '26', '37': '27', 'DE': '28', '12': '29', '72': '2A', 'BE': '2B', 'A7': '2C', '6B': '2D', '0B': '2E', 'C7': '2F', 'D3': '30', '1F': '31', '7F': '32', 'B3': '33', 'AA': '34', '66': '35', '06': '36', 'CA': '37', '23': '38', 'EF': '39', '8F': '3A', '43': '3B', '5A': '3C', '96': '3D', 'F6': '3E', '3A': '3F', '42': '40', '8E': '41', 'EE': '42', '22': '43', '3B': '44', 'F7': '45', '97': '46', '5B': '47', 'B2': '48', '7E': '49', '1E': '4A', 'D2': '4B', 'CB': '4C', '07': '4D', '67': '4E', 'AB': '4F', 'BF': '50', '73': '51', '13': '52', 'DF': '53', 'C6': '54', '0A': '55', '6A': '56', 'A6': '57', '4F': '58', '83': '59', 'E3': '5A', '2F': '5B', '36': '5C', 'FA': '5D', '9A': '5E', '56': '5F', '6C': '60', 'A0': '61', 'C0': '62', '0C': '63', '15': '64', 'D9': '65', 'B9': '66', '75': '67', '9C': '68', '50': '69', '30': '6A', 'FC': '6B', 'E5': '6C', '29': '6D', '49': '6E', '85': '6F', '91': '70', '5D': '71', '3D': '72', 'F1': '73', 'E8': '74', '24': '75', '44': '76', '88': '77', '61': '78', 'AD': '79', 'CD': '7A', '01': '7B', '18': '7C', 'D4': '7D', 'B4': '7E', '78': '7F',
       'C5': '80', '09': '81', '69': '82', 'A5': '83', 'BC': '84', '70': '85', '10': '86', 'DC': '87', '35': '88', 'F9': '89', '99': '8A', '55': '8B', '4C': '8C', '80': '8D', 'E0': '8E', '2C': '8F', '38': '90', 'F4': '91', '94': '92', '58': '93', '41': '94', '8D': '95', 'ED': '96', '21': '97', 'C8': '98', '04': '99', '64': '9A', 'A8': '9B', 'B1': '9C', '7D': '9D', '1D': '9E', 'D1': '9F', 'EB': 'A0', '27': 'A1', '47': 'A2', '8B': 'A3', '92': 'A4', '5E': 'A5', '3E': 'A6', 'F2': 'A7', '1B': 'A8', 'D7': 'A9', 'B7': 'AA', '7B': 'AB', '62': 'AC', 'AE': 'AD', 'CE': 'AE', '02': 'AF', '16': 'B0', 'DA': 'B1', 'BA': 'B2', '76': 'B3', '6F': 'B4', 'A3': 'B5', 'C3': 'B6', '0F': 'B7', 'E6': 'B8', '2A': 'B9', '4A': 'BA', '86': 'BB', '9F': 'BC', '53': 'BD', '33': 'BE', 'FF': 'BF', '87': 'C0', '4B': 'C1', '2B': 'C2', 'E7': 'C3', 'FE': 'C4', '32': 'C5', '52': 'C6', '9E': 'C7', '77': 'C8', 'BB': 'C9', 'DB': 'CA', '17': 'CB', '0E': 'CC', 'C2': 'CD', 'A2': 'CE', '6E': 'CF', '7A': 'D0', 'B6': 'D1', 'D6': 'D2', '1A': 'D3', '03': 'D4', 'CF': 'D5', 'AF': 'D6', '63': 'D7', '8A': 'D8', '46': 'D9', '26': 'DA', 'EA': 'DB', 'F3': 'DC', '3F': 'DD', '5F': 'DE', '93': 'DF', 'A9': 'E0', '65': 'E1', '05': 'E2', 'C9': 'E3', 'D0': 'E4', '1C': 'E5', '7C': 'E6', 'B0': 'E7', '59': 'E8', '95': 'E9', 'F5': 'EA', '39': 'EB', '20': 'EC', 'EC': 'ED', '8C': 'EE', '40': 'EF', '54': 'F0', '98': 'F1', 'F8': 'F2', '34': 'F3', '2D': 'F4', 'E1': 'F5', '81': 'F6', '4D': 'F7', 'A4': 'F8', '68': 'F9', '08': 'FA', 'C4': 'FB', 'DD': 'FC', '11': 'FD', '71': 'FE', 'BD': 'FF', }
LUT_INT = {int(k, 16): int(v, 16) for k, v in LUT.items()}


class TXSPacketDecoder:
    NO_FRAME_BYTES_OFFSET = 0
    HEADER_BYTES_OFFSET = 36
    HEADER_BYTES_SIZE = 6
    PAYLOAD_BYTES_OFFSET = 42
    PAYLOAD_BYTES_SIZE = 217

    IDLE_VIRTUAL_CHANNEL_ID = 0
    TAU_VIRTUAL_CHANNEL_ID = 1

    TAU_MAGIC = 0x01010202

    def __init__(self, packet_bytes):
        self.is_tau_packet = None
        if len(packet_bytes) != TXS_PACKET_LEN:
            raise ValueError(
                f'Invalid packet length: {len(packet_bytes)}, expected: f{TXS_PACKET_LEN}')
        self.packet_bytes = packet_bytes
        self._decode_packet()

    @staticmethod
    def _decode_bytes(bytes_):
        decoded_bytes = []
        for b in bytes_:
            decoded_bytes.append(LUT_INT[b])
        decoded_bytes = bytes(decoded_bytes)
        return decoded_bytes

    def _decode_header(self):
        self.header_bytes = self.packet_bytes[TXSPacketDecoder.HEADER_BYTES_OFFSET:
                                              TXSPacketDecoder.HEADER_BYTES_OFFSET + TXSPacketDecoder.HEADER_BYTES_SIZE]
        self.decoded_header_bytes = self._decode_bytes(self.header_bytes)
        virtual_channel_byte = self.decoded_header_bytes[1:2][0]
        self.virtual_channel_id = (virtual_channel_byte >> 1) & 7
        virt_channel_to_str = {
            TXSPacketDecoder.IDLE_VIRTUAL_CHANNEL_ID: 'Idle (0)',
            TXSPacketDecoder.TAU_VIRTUAL_CHANNEL_ID: 'TAU SAT2, I2C (1)',
            2: 'SPI (2)',
            3: 'Unknown (3)',
            4: 'Unknown (4)',
            5: 'Unknown (5)',
            6: 'Unknown (6)',
            7: 'Unknown (7)',
        }
        self.virtual_channel_id_str = virt_channel_to_str[self.virtual_channel_id]
        self.is_tau_packet = self.virtual_channel_id == TXSPacketDecoder.TAU_VIRTUAL_CHANNEL_ID

    def _decode_payload(self):
        self.payload_bytes = self.packet_bytes[TXSPacketDecoder.PAYLOAD_BYTES_OFFSET:
                                               TXSPacketDecoder.PAYLOAD_BYTES_OFFSET + TXSPacketDecoder.PAYLOAD_BYTES_SIZE]
        self.decoded_payload_bytes = self._decode_bytes(self.payload_bytes)

    def _decode_tau_payload(self):
        """Decodes TAU packets.

        Each TAU packet has the following structure:
        typedef struct inklajn_spl_TM
        {
            uint8_t type; //service type
            uint8_t subType; //service sub type
            unsigned short length;//Length of data array
            time_unix time;//Unix time
            byte data[SIZE_TXFRAME - SPL_TM_HEADER_SIZE];//the data in the packet
        }

        `time` is always filled with 0xdeadbeef magic.
               This allows us to identify our packets in high confidence.
        `length` - size in bytes, tells how many bytes are used in the `data` field.
        """
        assert hasattr(self, 'decoded_payload_bytes')

        TYPE_OFFSET = 0
        TYPE_SIZE = 1
        SUBTYPE_OFFSET = 1
        SUBTYPE_SIZE = 1
        LENGTH_OFFSET = 2
        LENGTH_SIZE = 2
        TIME_UNIX_OFFSET = 4
        TIME_SIZE = 4
        DATA_OFFSET = 8

        TOTAL_TAU_HEADER_SIZE = TYPE_SIZE + SUBTYPE_SIZE + LENGTH_SIZE + TIME_SIZE

        self.tau_type = struct.unpack(
            '<B', self.decoded_payload_bytes[TYPE_OFFSET:TYPE_OFFSET + TYPE_SIZE])[0]
        self.tau_subtype = struct.unpack(
            '<B', self.decoded_payload_bytes[SUBTYPE_OFFSET:SUBTYPE_OFFSET + SUBTYPE_SIZE])[0]
        self.tau_orig_length = struct.unpack(
            '<H', self.decoded_payload_bytes[LENGTH_OFFSET:LENGTH_OFFSET + LENGTH_SIZE])[0]
        self.tau_length = min(self.tau_orig_length, len(
            self.decoded_payload_bytes) - TOTAL_TAU_HEADER_SIZE)
        self.tau_time_unix = struct.unpack(
            '<I', self.decoded_payload_bytes[TIME_UNIX_OFFSET:TIME_UNIX_OFFSET + TIME_SIZE])[0]
        self.tau_data = self.decoded_payload_bytes[DATA_OFFSET:DATA_OFFSET + self.tau_length]

    def _decode_packet(self):
        assert len(self.packet_bytes) == TXS_PACKET_LEN
        self._decode_header()
        self._decode_payload()
        self._decode_tau_payload()

    @staticmethod
    def bytes_to_hexstr(bytes_):
        return ''.join('{:02x}'.format(b) for b in bytes_)

    def __str__(self):
        result = f"Packet type: {self.virtual_channel_id_str}\n"
        decoded_hex_bytes = TXSPacketDecoder.bytes_to_hexstr(
            self.decoded_payload_bytes)
        result += f"Payload: {self.decoded_payload_bytes}\n"

        if self.is_tau_packet and self.tau_time_unix == TXSPacketDecoder.TAU_MAGIC:
            result += "TAU packet info: \n"
            result += f"  Type: {self.tau_type}\n"
            result += f"  Sub type: {self.tau_subtype}\n"
            result += f"  Magic (unixtime): {'0x{:08x}'.format(self.tau_time_unix)}\n"
            result += f"  Length: {self.tau_length}, Orig Length: {self.tau_orig_length}\n"
            result += f"  Data: {TXSPacketDecoder.bytes_to_hexstr(self.tau_data)}\n"

        return result


def parse_args(argv):
    parser = ArgumentParser(
        description='Decodes one TXS packet.')
    parser.add_argument('packet', help='Path to a packet in binary form.')
    args = parser.parse_args(argv)
    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    print(f'Input file: {args.packet}')
    with open(args.packet, 'rb') as f:
        packet_data = f.read()
    txs_packet = TXSPacketDecoder(packet_data)
    print(str(txs_packet))


if __name__ == '__main__':
    main()
