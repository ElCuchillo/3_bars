import sys
import json
from math import cos, radians, sqrt


LONGITUDE, LATITUDE = 0, 1


def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def get_biggest_bar(bar_data):
    the_biggest_bar = (max(bar_data['features'], key=lambda x:
                           x['properties']['Attributes']['SeatsCount']))

    return the_biggest_bar


def get_smallest_bar(bar_data):
    the_smallest_bar = (min(bar_data['features'], key=lambda x:
                           x['properties']['Attributes']['SeatsCount']))

    return the_smallest_bar


def get_distance(source_point, some_bar):
    earth_radius= 6373
    delta_latitude = (radians(some_bar['geometry']['coordinates'][LATITUDE]
                              - source_point[LATITUDE]))
    delta_longitude = (radians(some_bar['geometry']['coordinates'][LONGITUDE]
                       - source_point[LONGITUDE]))
    ''' the formula for the distance is calculated by Lexander
        (lizz4mail@gmail.com)  based on Pifagorean theorem wit the assumptions
        that the Earth is round in general, and on the scale of the Moscow
        region it is flat.'''
    distance = (earth_radius * sqrt(delta_latitude ** 2
                                    + (delta_longitude
                                       * cos(radians(some_bar['geometry']
                                                             ['coordinates']
                                                             [LATITUDE])))
                                    ** 2))
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
    print('Для нахождения ближайшего бара введите текущие gps-координаты'
          'в десятичном формате.')
    try:
        longitude = float(input('долгота:'))
        latitude = float(input('широта:'))
        return longitude, latitude

    except ValueError:
        return 0, 0


def output_results(biggest_bar_attr, smallest_bar_attr, closest_bar_attr='',
                   min_distance=0):
    print('\nСамый большой бар - "{}, {}", {} мест'.
          format(biggest_bar_attr['properties']['Attributes']['Name'],
                 biggest_bar_attr['properties']['Attributes']['Address'],
                 biggest_bar_attr['properties']['Attributes']['SeatsCount']))
    print('\nСамый маленький бар - "{}, {}", {} мест'.
          format(smallest_bar_attr['properties']['Attributes']['Name'],
                 smallest_bar_attr['properties']['Attributes']['Address'],
                 smallest_bar_attr['properties']['Attributes']['SeatsCount']))
    if closest_bar_attr:
        print('\nБлижайший бар - "{}, {}", расстояние {:.2f} км'.
              format(closest_bar_attr['properties']['Attributes']['Name'],
                     closest_bar_attr['properties']['Attributes']['Address'],
                     min_distance))

    else:
        print('\nБлижайший бар найти не удалось, т.к. не введены '
              'текущие координаты.')


if __name__ == '__main__':
        try:
            bar_data = load_data(sys.argv[1])
            biggest_bar = get_biggest_bar(bar_data)
            smallest_bar = get_smallest_bar(bar_data)
            current_longitude, current_latitude = input_coordinates()
            closest_bar, min_distance = get_closest_bar(bar_data,
                                                        current_longitude,
                                                        current_latitude)
            output_results(biggest_bar, smallest_bar, closest_bar,
                           min_distance)
        except FileNotFoundError as error:
            print(error)
        except IndexError:
            print("Using: python3 bars.py <path to file>")
