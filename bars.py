import sys
import json
from math import cos, radians, sqrt


LONGITUDE = 0
LATITUDE = 1
EARTH_RADIUS = 6373


def load_data(filepath):
    with open(filepath, 'r') as loaded_data:
        return json.load(loaded_data)


def get_biggest_bar(json_data):
    the_biggest_bar = \
        max(json_data['features'],
            key=lambda x: x['properties']['Attributes']
            ['SeatsCount'])['properties']['Attributes']
    return the_biggest_bar


def get_smallest_bar(json_data):
    the_smallest_bar = \
        min(json_data['features'],
            key=lambda x: x['properties']['Attributes']
            ['SeatsCount'])['properties']['Attributes']
    return the_smallest_bar


def get_distance(source_point, some_bar):
    delta_latitude = radians(some_bar['geometry']['coordinates'][LATITUDE] - \
                             source_point[LATITUDE])
    delta_longitude = \
        radians(some_bar['geometry']['coordinates'][LONGITUDE]
                - source_point[LONGITUDE])
    ''' the formula for the distance is calculated by Lexander
        (lizz4mail@gmail.com)  based on Pifagorean theorem wit the assumptions
        that the Earth is round in general, and on the scale of the Moscow
        region it is flat.'''
    distance = EARTH_RADIUS * sqrt(delta_latitude ** 2 + \
                                   (delta_longitude *
                                    cos(radians(some_bar['geometry']
                                                ['coordinates']
                                                [LATITUDE]))) ** 2)
    return distance


def get_closest_bar(json_data, longitude, latitude):
    if not (longitude and latitude):
        return None, None
    current_point = [longitude, latitude]
    the_nearest_bar = min(json_data['features'],
                          key=lambda x: get_distance(current_point, x))
    distance = get_distance(current_point, the_nearest_bar)
    return the_nearest_bar['properties']['Attributes'], distance


def input_coordinates():
    print('Для нахождения ближайшего бара введите текущие gps-координаты'
          'в десятичном формате.')
    try:
        longitude = float(input('долгота:'))
        latitude = float(input('широта:'))
        return longitude, latitude

    except ValueError:
        return 0, 0


def output_results(biggest_bar, smallest_bar, closest_bar='', min_distance=0):
    print('\nСамый большой бар - "{}, {}", {} мест'.
          format(biggest_bar['Name'], biggest_bar['Address'],
                 biggest_bar['SeatsCount']))
    print('\nСамый маленький бар - "{}, {}", {} мест'.
          format(smallest_bar['Name'], smallest_bar['Address'],
                 smallest_bar['SeatsCount']))
    if closest_bar:
        print('\nБлижайший бар - "{}, {}", расстояние {:.2f} км'.
              format(closest_bar['Name'], closest_bar['Address'],
                     min_distance))

    else:
        print('\nБлижайший бар найти не удалось, т.к. не введены '
              'текущие координаты.')


if __name__ == '__main__':
        try:
            json_data = load_data(sys.argv[1])
            biggest_bar = get_biggest_bar(json_data)
            smallest_bar = get_smallest_bar(json_data)
            current_longitude, current_latitude = input_coordinates()
            closest_bar, min_distance = get_closest_bar(json_data,
                                                        current_longitude,
                                                        current_latitude)
            output_results(biggest_bar, smallest_bar,
                               closest_bar, min_distance)
        except FileNotFoundError as error:
            print(error)
        except IndexError:
            print("Using: python3 bars.py <path to file>")
