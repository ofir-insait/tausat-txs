from txs_packet_decoder import TXSPacketDecoder


def test_virtual_channel_decode_all_ones():
    paths = ["packets/idle_packet_0.bin",
             "packets/idle_packet_1.bin",
             "packets/idle_packet_2.bin"]
    for path in paths:
        with open(path, 'rb') as f:
            packet_data = f.read()
        txs_packet = TXSPacketDecoder(packet_data)
        assert txs_packet.virtual_channel_id == 0

    paths = ["packets/tausat2_virtual_channel_id_6_0.bin",
             "packets/tausat2_virtual_channel_id_6_1.bin",
             "packets/tausat2_virtual_channel_id_6_2.bin"]
    for path in paths:
        with open(path, 'rb') as f:
            packet_data = f.read()
        txs_packet = TXSPacketDecoder(packet_data)
        assert txs_packet.virtual_channel_id == 6

    paths = ["packets/tausat2_virtual_channel_id_1_0.bin",
             "packets/tausat2_virtual_channel_id_1_1.bin",
             "packets/tausat2_virtual_channel_id_1_2.bin"]
    for path in paths:
        with open(path, 'rb') as f:
            packet_data = f.read()
        txs_packet = TXSPacketDecoder(packet_data)
        assert txs_packet.virtual_channel_id == 1


def test_virtual_channel_decode_counter_0_to_29():
    paths = ["packets/tausat2_counter_0_to_29.bin"]
    for path in paths:
        with open(path, 'rb') as f:
            packet_data = f.read()
        txs_packet = TXSPacketDecoder(packet_data)
        assert txs_packet.virtual_channel_id == 1
        assert txs_packet.decoded_payload_bytes[:30] == bytes([0x1]) * 30
        total_len = 30
        assert txs_packet.decoded_payload_bytes[30:30 + total_len] == bytes(
            range(0, 30))


def test_virtual_channel_decode_counter_30_to_149():
    paths = ["packets/tausat2_counter_30_to_149.bin"]
    for path in paths:
        with open(path, 'rb') as f:
            packet_data = f.read()
        txs_packet = TXSPacketDecoder(packet_data)
        assert txs_packet.virtual_channel_id == 1
        assert txs_packet.decoded_payload_bytes[:30] == bytes([0x1]) * 30
        assert txs_packet.decoded_payload_bytes[30:150] == bytes(
            range(30, 150))


def test_virtual_channel_decode_counter_150_to_255():
    paths = ["packets/tausat2_counter_150_to_255.bin"]
    for path in paths:
        with open(path, 'rb') as f:
            packet_data = f.read()
        txs_packet = TXSPacketDecoder(packet_data)
        assert txs_packet.virtual_channel_id == 1
        assert txs_packet.decoded_payload_bytes[:30] == bytes([0x1]) * 30
        total_len = 255 - 150 + 1
        assert txs_packet.decoded_payload_bytes[30:30 + total_len] == bytes(
            range(150, 256))


def test_prefix_length_and_magic_decoding():
    paths = ["packets/tausat2_prefix_length_packet_30_ones.bin"]
    for path in paths:
        with open(path, 'rb') as f:
            packet_data = f.read()
        txs_packet = TXSPacketDecoder(packet_data)
        assert txs_packet.virtual_channel_id == 1
        assert txs_packet.tau_type == 1
        assert txs_packet.tau_subtype == 2
        assert txs_packet.tau_length == 30
        assert txs_packet.tau_time_unix == 0x01010202
        assert txs_packet.tau_length == len(txs_packet.tau_data)
        assert txs_packet.tau_data == bytes([1]) * 30
