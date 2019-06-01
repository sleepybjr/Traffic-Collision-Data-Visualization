import geocoder
import csv
import re

CITY = 'San Diego'
STATE = 'California'

url = 'http://<local-osm-url-here>/'


def send_address(address):
    full_address = f'{address}, {CITY} {STATE}'
    output = geocoder.osm(full_address, url=url)

    # some locaitons dont have results
    if len(output) == 0:
        print(full_address)
        return None, None
    return output.latlng


def read_collisions(input_filename, output_filename):
    with open(input_filename) as read_file, open(output_filename, "w") as write_file:
        csv_reader = csv.reader(read_file, delimiter=',')
        count = filter1 = filter2 = 0
        for row in csv_reader:
            if count:
                street_num = row[3]
                street_dir = ' {} '.format(row[4]) if row[4] != ' ' else ' '
                street_name = row[5]
                if 'CAM' in street_name:
                    street_name = street_name.replace('CAM ', 'CAMINO ')
                if re.match(r'0[1-9][A-Z]{2}', street_name):
                    street_name = street_name[1:]

                street_type = row[6]

                if row[3] == '0':
                    filter1 += 1
                    continue

                address = f'{street_num}{street_dir}{street_name} {street_type}'

                latitude, longitude = send_address(address)
                if latitude and longitude:
                    write_file.write(f'{latitude}, {longitude}\n')
                else:
                    filter2 += 1
                    continue

            else:
                write_file.write('y_lat, x_lng\n')

            count += 1

        print(f'Total records: {count}\nFilter By No Address: {filter1}\nFilter by Not Found By OSM: {filter2}')


if __name__ == '__main__':
    read_collisions(input_filename='pd_collisions_datasd.csv', output_filename='latlng.csv')

