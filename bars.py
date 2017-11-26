import sys
import json
from math import cos, radians, sqrt


LONGITUDE = 0
LATITUDE = 1
EARTH_RADIUS = 6373


def load_data(filepath):
    try:
        with open(filepath, 'r') as loaded_data:
            return json.load(loaded_data)
    except FileNotFoundError:
        return None


def get_biggest_bar(json_data):
    the_biggest_bar = \
        max(json_data['features'],
            key=lambda x: x['properties']['Attributes']['SeatsCount'])
    bar_ID = the_biggest_bar['properties']['Attributes']['global_id']
    return bar_ID


def get_smallest_bar(json_data):
    the_smallest_bar = \
        min(json_data['features'],
            key=lambda x: x['properties']['Attributes']['SeatsCount'])
    bar_ID = the_smallest_bar['properties']['Attributes']['global_id']
    return bar_ID


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
    current_point = [longitude, latitude]

    the_nearest_bar = min(json_data['features'],
                          key=lambda x: get_distance(current_point,x))
    bar_ID = the_nearest_bar['properties']['Attributes']['global_id']
    distance = get_distance(current_point, the_nearest_bar)
    return bar_ID, distance


def input_coordinates():
    print('Для нахождения ближайшего бара введите текущие gps-координаты'
          'в десятичном формате.')
    try:
        longitude = float(input('долгота:'))
        latitude = float(input('широта:'))
        return longitude, latitude

    except ValueError:
        return 0, 0


def get_bar_description(json_data, bar_ID):

    bar_attributes = [bar['properties']['Attributes']
                      for bar in json_data['features']
                      if bar['properties']['Attributes']
                      ['global_id'] == bar_ID][0]

    return bar_attributes


def output_results(json_data, the_biggest_ID, the_smallest_ID,
                           the_closest_ID='', min_distance=0):
    biggest_bar = get_bar_description(json_data, the_biggest_ID)
    print('\nСамый большой бар - "{}, {}", {} мест'.
          format(biggest_bar['Name'], biggest_bar['Address'],
                 biggest_bar['SeatsCount']))

    smallest_bar = get_bar_description(json_data, the_smallest_ID)
    print('\nСамый маленький бар - "{}, {}", {} мест'.
          format(smallest_bar['Name'], smallest_bar['Address'],
                 smallest_bar['SeatsCount']))


    if the_closest_ID:
        closest_bar = get_bar_description(json_data, the_closest_ID)
        print('\nБлижайший бар - "{}, {}", расстояние {:.2f} км'.
              format(closest_bar['Name'], closest_bar['Address'],
                     min_distance))

    else:
        print('\nБлижайший бар найти не удалось, т.к. не введены '
              'текущие координаты.')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        json_data = load_data(sys.argv[1])
        if json_data:
            biggest_bar_ID = get_biggest_bar(json_data)
            smallest_bar_ID = get_smallest_bar(json_data)
            current_longitude, current_latitude = input_coordinates()

            if current_longitude and current_latitude:
                closest_bar_ID, min_distance = get_closest_bar(json_data,
                                                   current_longitude,
                                                   current_latitude)
                output_results(json_data, biggest_bar_ID, smallest_bar_ID,
                               closest_bar_ID, min_distance)
            else:
                output_results(json_data, biggest_bar_ID, smallest_bar_ID)
        else:
            print("File or directory {} not found".format(sys.argv[1]))
    else:
        print("Using: python3 bars.py <path to file>")
