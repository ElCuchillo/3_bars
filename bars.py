import sys
import json
from math import cos, radians, sqrt


def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def get_biggest_bar(bar_data):
    the_biggest_bar = max(bar_data['features'],
                          key=lambda x: x['properties']['Attributes']
                                         ['SeatsCount'])
    return the_biggest_bar


def get_smallest_bar(bar_data):
    the_smallest_bar = min(bar_data['features'],
                           key=lambda x: x['properties']['Attributes']
                                          ['SeatsCount'])

    return the_smallest_bar


def get_distance(source_point, some_bar):
    longitude, latitude = 0, 1
    earth_radius = 6373

    delta_latitude = (radians(some_bar['geometry']['coordinates'][latitude]
                      - source_point[latitude]))
    delta_longitude = (radians(some_bar['geometry']['coordinates'][longitude]
                       - source_point[longitude]))
    # the formula for the distance is calculated by Lexander
    #    (lizz4mail@gmail.com)  based on Pifagorean theorem wit the assumptions
    #    that the Earth is round in general, and on the scale of the Moscow
    #    region it is flat.

    distance = (earth_radius * sqrt(delta_latitude ** 2
        + (delta_longitude * cos(radians(some_bar['geometry']['coordinates']
            [latitude]))) ** 2))
    return distance


def get_closest_bar(bar_data, longitude, latitude):
    if not (longitude and latitude):
        return None, None
    current_point = [longitude, latitude]
    the_nearest_bar = min(bar_data['features'],
                          key=lambda x: get_distance(current_point, x))
    distance = get_distance(current_point, the_nearest_bar)
    return the_nearest_bar, distance


def input_coordinates():
    print('\nДля нахождения ближайшего бара введите текущие gps-координаты'
          ' в десятичном формате.')
    try:
        longitude = float(input('долгота:'))
        latitude = float(input('широта:'))
        return longitude, latitude
    except ValueError:
        print('\nНеверный формат gps-координат')
        return None, None


def print_bar_info(some_bar, bar_type, min_distance=None):
    if not some_bar:
        message = '\nБлижайший бар найти не удалось, т.к. не введены ' \
                  'текущие координаты.'
    else:
        bar_attributes = (some_bar['properties']['Attributes']['Name'],
                          some_bar['properties']['Attributes']['Address'],
                          some_bar['properties']['Attributes']['SeatsCount'])
        message = '\n{0} бар - "{1[0]}, {1[1]}", '.format(bar_type,
                                                          bar_attributes)
        if min_distance:
            message += 'расстояние {:.2f}км'.format(min_distance)
        else:
            message += '{} мест'.format(bar_attributes[2])
    print(message)


if __name__ == '__main__':
    try:
        bar_data = load_data(sys.argv[1])
        biggest_bar = get_biggest_bar(bar_data)
        print_bar_info(biggest_bar, 'Самый большой')
        smallest_bar = get_smallest_bar(bar_data)
        print_bar_info(smallest_bar, 'Самый маленький')
        current_longitude, current_latitude = input_coordinates()
        closest_bar, min_distance = get_closest_bar(bar_data,
                                                    current_longitude,
                                                    current_latitude)
        print_bar_info(closest_bar, 'Ближайший', min_distance)

    except FileNotFoundError as error:
        print(error)
    except IndexError:
        print("Использование: python3 bars.py <path to file>")
