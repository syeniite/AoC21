from collections import namedtuple

Target = namedtuple("Target", "min_x max_x min_y max_y")


def get_max_y_velocity(target_min_y):
    if target_min_y > 0:
        return (target_min_y*(target_min_y+1)) // 2
    else:
        return ((-target_min_y-1)*(-target_min_y)) // 2


def brute_force_all(target: Target):
    all_velocities = []
    for x in range(target.max_x+1):
        for y in range(target.min_y-1, -target.min_y):
            if can_reach_target_area([x, y], target):
                all_velocities.append((x, y))

    return all_velocities


def can_reach_target_area(vel, target):
    def update_x(vel_x):
        if vel_x == 0:
            return 0
        if vel_x > 0:
            return vel_x - 1
        return vel_x + 1

    def update_y(vel_y):
        return vel_y - 1

    def is_in_area(x, y):
        return target.min_x <= x <= target.max_x and target.min_y <= y <= target.max_y

    step = 0
    curr_x, curr_y = 0, 0

    while curr_x <= target.max_x and curr_y >= target.min_y:
        if is_in_area(curr_x, curr_y):
            return True
        curr_x += vel[0]
        curr_y += vel[1]

        vel[0] = update_x(vel[0])
        vel[1] = update_y(vel[1])

        step += 1

    return False


if __name__ == '__main__':
    t = Target(277, 318, -92, -53)
    # t = Target(20, 30, -10, -5)
    all_vels = brute_force_all(t)
    print(len(all_vels))
