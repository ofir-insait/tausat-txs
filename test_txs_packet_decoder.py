from txs_packet_decoder import TXSPacketDecoder


def test_virtual_channel_decode():
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
