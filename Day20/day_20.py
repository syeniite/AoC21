def read_file(file_name):
    with open(file_name, "r") as f:
        enhancement = [encoding for encoding in f.readline().strip()]
        f.read(1)
        image = [[pixel for pixel in line.strip()] for line in f.readlines()]

        return enhancement, image


def enhance(enhancement_table, image, boundary_pixel='.'):
    enhanced_image = [[get_enhancement_encoding(image, i, j, boundary_pixel, enhancement_table)
                       for j in range(-1, len(image[0])+1)] for i in range(-1, len(image)+1)]
    new_boundary_pixel = enhancement_table[get_encoding_number([boundary_pixel for _ in range(9)])]

    return enhanced_image, new_boundary_pixel


def get_encoding_number(pixels):
    encoding_number = 0

    for pos, pixel in enumerate(reversed(pixels)):
        if pixel == '#':
            encoding_number |= 1 << pos

    return encoding_number


def get_enhancement_encoding(image, i, j, boundary_pixel, enhancement_table):
    def get_surrounding_indices():
        return (i - 1, j - 1), (i - 1, j), (i - 1, j + 1), \
               (i, j - 1), (i, j), (i, j + 1), \
               (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)

    def is_in_core_image(y, x):
        return 0 <= y < len(image) and 0 <= x < len(image[0])

    surrounding_pixels = [image[k][l] if is_in_core_image(k, l) else boundary_pixel
                          for k, l in get_surrounding_indices()]

    return enhancement_table[get_encoding_number(surrounding_pixels)]


def count_pixels_lit(image):
    return sum(sum([1 if pixel == '#' else 0 for pixel in line]) for line in image)


def pprint_matrix(m):
    for i in range(len(m)):
        for j in range(len(m[0])):
            print(m[i][j], end="")
        print()
    print()


def enhance_n_times(enhancement_table, image, n):
    boundary = '.'
    for _ in range(n):
        image, boundary = enhance(enhancement_table, image, boundary_pixel=boundary)

    return image


if __name__ == '__main__':
    _enhancement, img = read_file("input.txt")
    # pprint_matrix(img)
    enhanced = enhance_n_times(_enhancement, img, 50)
    # pprint_matrix(enhanced)
    print(count_pixels_lit(enhanced))
