from expression import PacketType, Expression


sum_versions = 0


def count_versions(bits):
    global sum_versions
    read_packet(bits, 0)

    versions = sum_versions
    sum_versions = 0

    return versions


def parse(bits):
    expr, index = read_packet(bits, 0)
    print(expr)
    return expr.evaluate()


def read_packet(bits, current_index):
    global sum_versions
    version, current_index = read_packet_version(bits, current_index)
    packet_id, current_index = read_packet_id(bits, current_index)

    sum_versions += version
    expression = Expression(PacketType(packet_id))
    if packet_id == PacketType.LITERAL.value:
        literal, current_index = read_literal_value(bits, current_index)
        expression.args.append(literal)
    else:
        arguments, current_index = read_operator_packet(bits, current_index)
        expression.args += arguments

    return expression, current_index


def read_packet_version(bits, current_index):
    return convert_bits_to_int(bits[current_index:current_index+3]), current_index + 3


def read_packet_id(bits, current_index):
    return read_packet_version(bits, current_index)


def read_literal_value(bits, current_index, group_length_with_prefix=5):
    def read_group(curr):
        for index in range(curr, curr + group_length_with_prefix - 1):
            value_bits.append(bits[index])

    value_bits = []

    while True:
        read_group(current_index+1)

        if not bits[current_index]:
            current_index += group_length_with_prefix
            break
        current_index += group_length_with_prefix

    return convert_bits_to_int(value_bits), current_index


def read_operator_packet(bits, current_index):
    # an operator packet can have two different length types: total length in bits or number of sub-packets
    def read_total_length_in_bits(curr, length=15):
        return convert_bits_to_int([bits[i] for i in range(curr, curr+length)]), curr + length

    def read_number_of_sub_packets(curr, length=11):
        return convert_bits_to_int([bits[i] for i in range(curr, curr+length)]), curr + length

    is_total_length_in_bits = not bits[current_index]
    current_index += 1
    arguments = []

    if is_total_length_in_bits:
        total_length_in_bits, current_index = read_total_length_in_bits(current_index)
        index_after_all_packets = current_index + total_length_in_bits

        while current_index < index_after_all_packets:
            expression, current_index = read_packet(bits, current_index)
            arguments.append(expression)

    else:
        number_of_sub_packets, current_index = read_number_of_sub_packets(current_index)

        for _ in range(number_of_sub_packets):
            expression, current_index = read_packet(bits, current_index)
            arguments.append(expression)

    return arguments, current_index


def convert_bits_to_int(bits):
    out = 0
    for bit in bits:
        out = (out << 1) | bit

    return out


def read_file(file_name):
    with open(file_name, "r") as f:
        return hex_string_to_bits(f.read().strip())


def hex_string_to_bits(hex_string):
    return [byte & (1 << (7-j)) > 0 for byte in bytearray.fromhex(hex_string) for j in range(8)]


def show_index(bits, index):
    print(''.join([str(int(b)) for b in bits]))
    print(" "*index + "^")


if __name__ == '__main__':
    bit_list = read_file("input.txt")
    print(parse(bit_list))
