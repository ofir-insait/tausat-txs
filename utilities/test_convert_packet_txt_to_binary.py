import os

from convert_packet_txt_to_binary import read_packet_txt_from_path, convert_packet_txt_to_binary


def test_txt_to_bin_conversion():
    paths = ["packets/idle_packet_0.txt",
             "packets/idle_packet_1.txt",
             "packets/idle_packet_2.txt",
             "packets/tausat2_virtual_channel_id_6_0.txt",
             "packets/tausat2_virtual_channel_id_6_1.txt",
             "packets/tausat2_virtual_channel_id_6_2.txt",
             "packets/tausat2_virtual_channel_id_1_0.txt",
             "packets/tausat2_virtual_channel_id_1_1.txt",
             "packets/tausat2_virtual_channel_id_1_2.txt",
             "packets/tausat2_counter_0_to_29.txt",
             "packets/tausat2_counter_30_to_149.txt",
             "packets/tausat2_counter_150_to_255.txt",
             "packets/tausat2_prefix_length_packet_30_ones.txt"]
    for path in paths:
        path_ = os.path.join(os.path.dirname(__file__), os.pardir, path)
        line = read_packet_txt_from_path(path_)
        dst = convert_packet_txt_to_binary(path)
        with open(dst, 'rb') as f:
            data = f.read()
        assert len(data) == 259
        #print(f'Packet length: {len(data)}')
        decoded_line = ''.join('{:02x}'.format(d) for d in data)
        assert line == decoded_line
