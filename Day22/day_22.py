from collections import namedtuple
from time import perf_counter
Cuboid = namedtuple("Cuboid", "x_range y_range z_range, volume_sign")
Instruction = namedtuple("Instruction", "active cuboid")


def read_instructions(file_name):
    def parse_line(line):
        state, cuboid = line.split(" ")
        ranges = [r.split("..") for r in cuboid.split(",")]
        return Instruction(
            active=state == "on",
            cuboid=Cuboid(
                x_range=(int(ranges[0][0].split("=")[1]), int(ranges[0][1])),
                y_range=(int(ranges[1][0].split("=")[1]), int(ranges[1][1])),
                z_range=(int(ranges[2][0].split("=")[1]), int(ranges[2][1])),
                volume_sign=1 if state == "on" else -1
            )
        )

    with open(file_name, "r") as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def get_intersection_cuboid(cuboid, other):
    # other = already existing cuboid,
    # cuboid = newly introduced cuboid
    #
    # volume_sign=-other.volume_sign deserves an explanation:
    # the whole idea is to add all active cubes together and subtract the intersections and inactive volumes
    # but since more than two cuboids can intersect and new intersections can yet intersect intersections (heh)
    # we have to decide when to add or when to subtract an intersection.
    # Intersection table:
    #  cuboid | other  | result
    # ------------------------
    #  active | active |   -
    # inactive| active |   -
    #  active |inactive|   +
    # inactive|inactive|   +
    #
    # so it basically only depends on the volume sign of the other cuboid => negate the volume sign of the other cuboid

    if share_range(cuboid.x_range, other.x_range) and share_range(cuboid.y_range, other.y_range) \
            and share_range(cuboid.z_range, other.z_range):

        return Cuboid(x_range=get_shared_range(cuboid.x_range, other.x_range),
                      y_range=get_shared_range(cuboid.y_range, other.y_range),
                      z_range=get_shared_range(cuboid.z_range, other.z_range),
                      volume_sign=-other.volume_sign)
    return None


def share_range(range_1, range_2):
    return range_1[0] <= range_2[1] and range_2[0] <= range_1[1]


def get_shared_range(range_1, range_2):
    return max(range_1[0], range_2[0]), min(range_1[1], range_2[1])


def reboot_cubes(instructions):
    # the first instruction doesn't have to be an activation instruction but luckily the input is nice to us, so
    # we don't test anything here.
    # this is a horrible exponential worst-case algorithm but who cares :)
    # a plane sweep algorithm should be possible, but it is very complicated
    # also, with coordinate compression a O(n^3) algorithm can be worked out.
    current_cuboids = []

    for instruction in instructions:
        intersections = []
        for cuboid in current_cuboids:
            if intersection := get_intersection_cuboid(instruction.cuboid, cuboid):
                intersections.append(intersection)

        current_cuboids += intersections

        if instruction.active:
            current_cuboids.append(instruction.cuboid)

    return sum(cuboid.volume_sign * get_number_of_cubes(cuboid) for cuboid in current_cuboids)


def get_number_of_cubes(cuboid):
    return (cuboid.x_range[1] - cuboid.x_range[0]+1)*(cuboid.y_range[1] - cuboid.y_range[0]+1)\
           * (cuboid.z_range[1] - cuboid.z_range[0]+1)


def is_in_range(some_range):
    return -50 <= some_range[0] <= 51 and -50 <= some_range[1] <= 51


if __name__ == '__main__':
    all_instructions = read_instructions("input.txt")
    # print(all_instructions)
    # all_instructions = [Instruction(activate=True, cuboid=Cuboid([0, 10], [0, 10], [0, 10])),
    #                     Instruction(activate=False, cuboid=Cuboid([-9, 1], [-9, 1], [-9, 1]))]
    t1 = perf_counter()
    print(reboot_cubes(all_instructions))
    print(f"time elapsed: {perf_counter()-t1:.3f}s")
