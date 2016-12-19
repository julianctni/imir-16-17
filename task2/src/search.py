import os
import math
import webbrowser
from sys import platform
from collections import defaultdict
from utilities import open_file, get_base_dir, saveResult
from analyze import createDescriptor
from buildIndex import getContentType


def calculate_distance(first_image, second_image):
    y_dc_1, y_ac_1, cb_dc_1, cb_ac_1, cr_dc_1, cr_ac_1 = first_image
    y_dc_2, y_ac_2, cb_dc_2, cb_ac_2, cr_dc_2, cr_ac_2 = second_image

    d_y_1 = [y_dc_1] + y_ac_1
    d_cb_1 = [cb_dc_1] + cb_ac_1
    d_cr_1 = [cr_dc_1] + cr_ac_1

    d_y_2 = y_dc_2 + y_ac_2
    d_cb_2 = cb_dc_2 + cb_ac_2
    d_cr_2 = cr_dc_2 + cr_ac_2

    distance_d_y = math.sqrt(sum(pow(x - y, 2) for x, y in zip(d_y_1, d_y_2)))
    distance_d_cb = math.sqrt(sum(pow(x - y, 2) for x, y in zip(d_cb_1, d_cb_2)))
    distance_d_cr = math.sqrt(sum(pow(x - y, 2) for x, y in zip(d_cr_1, d_cr_2)))

    distance = distance_d_y + distance_d_cb + distance_d_cr

    return distance


def search(image_path, index):
    image_content_type = getContentType(image_path.replace("jpg", "xml"))
    image_descriptors = createDescriptor(image_path)

    filtered_index = index[image_content_type]

    results = []
    for image in filtered_index:
        image_id = image["image_id"]
        descriptors = (image["y_dc"], image["y_ac"], image["cb_dc"], image["cb_ac"], image["cr_dc"], image["cr_ac"])
        distance = calculate_distance(image_descriptors, descriptors)
        # Add tuple that contains the image id and the distance to the results list.
        # The image id is necessary to reference the most similar image to the user.
        results.append((image_id, distance))

    # Sort the tuples in the results list by the second item of the tuple (= distance).
    sorted_results = sorted(results, key=lambda x: x[1])

    print("Number of images of type %s: %i" % (image_content_type, len(filtered_index)))

    return sorted_results


def parse_index():
    index_file_path = os.path.join(get_base_dir(), 'assets/index.csv')
    index_file = open_file(index_file_path)
    index_lines = index_file.read().splitlines()
    index_count = len(index_lines)

    index = defaultdict(list)
    for i in range(0, index_count):
        index_line = index_lines[i]
        content = index_line.split(",")
        # The first word in an index line is the content type of one particular image.
        content_type = content[0]
        # The AC coefficients are grouped and separated from each other by a single whitespace.
        string_coefficients = [x.split() for x in content[1:-1]]
        # Convert the list of coefficients, which are still of type string, into a list of floats.
        coefficients = [[float(y) for y in x] for x in string_coefficients]
        # The last word in an index line is the image id
        image_id = int(content[-1])

        y_dc, y_ac, cb_dc, cb_ac, cr_dc, cr_ac = coefficients

        index[content_type].append({
            'image_id': image_id,
            'y_dc': y_dc,
            'cb_dc': cb_dc,
            'cr_dc': cr_dc,
            'y_ac': y_ac,
            'cb_ac': cb_ac,
            'cr_ac': cr_ac
        })

    return index


def perform_search(image_path):
    index = parse_index()
    return search(image_path, index)


def main():
    directory = os.path.join(get_base_dir(), "PlantCLEF2016Test/")
    index = parse_index()

    while True:
        image_name = input("Enter image name: ")
        image_path = os.path.join(directory, image_name)

        search_results = search(image_path, index)

        # Get the image id from the second lowest distance. The lowest distance is the searched image itself.
        lowest_distance_id = search_results[1][0]
      
        print("Most similar picture with id: %i" % lowest_distance_id)

        results_file_path = saveResult(search_results)

        # check if on OSX
        if platform == "darwin":
            results_file_path = "file:///" + results_file_path

        webbrowser.get().open(results_file_path)


if __name__ == "__main__":
    main()
