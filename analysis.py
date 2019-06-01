import csv


def analyze_times(input_filename):
    split_hours = {i: [0, 0, 0] for i in range(24)}

    with open(input_filename) as read_file:
        csv_reader = csv.reader(read_file, delimiter=',')
        first_row = False
        for row in csv_reader:
            if first_row:
                date, time = row[1].split(' ', 1)
                hour = time.split(':')[0]
                split_hours[int(hour)][0] += 1  # collisions
                split_hours[int(hour)][1] += int(row[-3])  # injuries
                split_hours[int(hour)][2] += int(row[-2])  # deaths
            else:
                first_row = True

    for hour, amount in split_hours.items():
        print(f'Hour: {hour}, Amount Of Collisions: {amount[0]}, '
              f'Amount Of Injuries: {amount[1]}, '
              f'Amount Of Deaths: {amount[2]}')


if __name__ == '__main__':
    analyze_times(input_filename='pd_collisions_datasd.csv')
