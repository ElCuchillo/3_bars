import sys
import json
from math import cos, radians, sqrt


LONGITUDE = 0
LATITUDE = 1
SEATS = 2
EARTH_RADIUS = 6373


def load_data(filepath):
    try:
        with open(filepath, 'r') as loaded_data:
            return json.load(loaded_data)
    except FileNotFoundError:
        return None


def parse_data(parsed_data):
    all_bars_dict = {}
    for bar_info in parsed_data['features']:
        bar_name = bar_info['properties']['Attributes']['Name'] + ', ' + \
                   bar_info['properties']['Attributes']['Address']
        bar_options = [bar_info['geometry']['coordinates'][LONGITUDE], \
                       bar_info['geometry']['coordinates'][LATITUDE], \
                       bar_info['properties']['Attributes']['SeatsCount']
                       ]
        all_bars_dict.update({bar_name: bar_options})
    return all_bars_dict


def get_biggest_bar(bars_data):
    return max(bars_data, key=lambda x: bars_data[x][SEATS])


def get_smallest_bar(bars_data):
    return min(bars_data, key=lambda x: bars_data[x][SEATS])


def get_distance(source_point, some_bar):
    delta_latitude = radians(some_bar[LATITUDE] - source_point[LATITUDE])
    delta_longitude = radians(some_bar[LONGITUDE] - \
                              source_point[LONGITUDE])
    distance = EARTH_RADIUS * sqrt(delta_latitude ** 2 + \
                                   (delta_longitude * \
                                    cos(radians(some_bar[LATITUDE]))) ** 2)
    return distance


def get_closest_bar(bars_data, longitude, latitude):
    current_point = [longitude, latitude]
    return min(bars_data, key=lambda x: get_distance(current_point,
                                                     bars_data[x]))

def input_coordinates():
    print('Для нахождения ближайшего бара введите текущие gps-координаты'
          'в десятичном формате.')
    try:
        longitude = float(input('долгота:'))
        latitude = float(input('широта:'))
        return longitude, latitude

    except ValueError:
        return 0, 0


def output_results(all_bars_dict, the_biggest, the_smallest,
                           the_closest='', min_distance=0):
    print('\nСамый большой бар - "{}", {} мест'.
          format(the_biggest, all_bars_dict[the_biggest][SEATS]))
    print('\nСамый маленький бар - "{}", {} мест'.
          format(the_smallest, all_bars_dict[the_smallest][SEATS]))
    if the_closest:
        print('\nБлижайший бар - "{}", расстояние {:.2f} км'.
               format(the_closest, min_distance))
    else:
        print('\nБлижайший бар найти не удалось, т.к. не введены '
              'текущие координаты.')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        loaded_data = load_data(sys.argv[1])
        if loaded_data:
            all_bars_dict = parse_data(loaded_data)
            the_biggest = get_biggest_bar(all_bars_dict)
            the_smallest = get_smallest_bar(all_bars_dict)
            current_longitude, current_latitude = input_coordinates()

            if current_longitude and current_latitude:
                the_closest = get_closest_bar(all_bars_dict,
                                              current_longitude,
                                              current_latitude)
                current_point = [current_longitude,current_latitude]
                min_distance = get_distance(current_point,
                                        all_bars_dict[the_closest])
                output_results(all_bars_dict, the_biggest, the_smallest,
                               the_closest, min_distance)
            else:

                output_results(all_bars_dict, the_biggest, the_smallest)

        else:
            print("File or directory {} not found".format(sys.argv[1]))
    else:
        print("Using: python3 bars.py <path to file>")
