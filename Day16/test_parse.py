import unittest
from day_16 import count_versions, hex_string_to_bits, parse


class TestDay16Parse(unittest.TestCase):
    def test_parse_version_count(self):
        versions = count_versions(hex_string_to_bits("8A004A801A8002F478"))
        self.assertEqual(16, versions)

        versions = count_versions(hex_string_to_bits("620080001611562C8802118E34"))
        self.assertEqual(12, versions)

        versions = count_versions(hex_string_to_bits("C0015000016115A2E0802F182340"))
        self.assertEqual(23, versions)

        versions = count_versions(hex_string_to_bits("A0016C880162017C3686B18A3D4780"))
        self.assertEqual(31, versions)

    def test_parse(self):
        result = parse(hex_string_to_bits("C200B40A82"))
        self.assertEqual(3, result)

        result = parse(hex_string_to_bits("04005AC33890"))
        self.assertEqual(54, result)

        result = parse(hex_string_to_bits("880086C3E88112"))
        self.assertEqual(7, result)

        result = parse(hex_string_to_bits("CE00C43D881120"))
        self.assertEqual(9, result)

        result = parse(hex_string_to_bits("D8005AC2A8F0"))
        self.assertEqual(True, result)

        result = parse(hex_string_to_bits("F600BC2D8F"))
        self.assertEqual(False, result)

        result = parse(hex_string_to_bits("9C005AC2F8F0"))
        self.assertEqual(False, result)

        result = parse(hex_string_to_bits("9C0141080250320F1802104A08"))
        self.assertEqual(True, result)


if __name__ == '__main__':
    unittest.main()
