import os
import csv

CAR_TYPE = 0
BRAND = 1
PASS_SEATS = 2
PHOTO = 3
BODY_WHL = 4
CARRYING = 5
EXTRA = 6


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        try:
            return os.path.splitext(self.photo_file_name)[1]
        except IndexError:
            return 'wrong file'


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)
        self.car_type = 'car'


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'truck'
        try:
            self.body_length, self.body_width, self.body_height,  = map(float, body_whl.split('x'))
        except ValueError:
            self.body_width, self.body_height, self.body_length = 0.0, 0.0, 0.0

    def get_body_volume(self):
        return self.body_width * self.body_length * self.body_height


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = 'spec_machine'


def get_photo_carrying(row):
    float(row[CARRYING])
    first, _ = row[PHOTO].split('.')
    if len(row[BRAND]) == 0 or not first:
        raise ValueError


def check_car(row):
    try:
        int(row[PASS_SEATS])
        get_photo_carrying(row)
    except ValueError:
        return None
    else:
        return Car(row[BRAND], row[PHOTO], row[CARRYING], row[PASS_SEATS])


def check_truck(row):
    try:
        get_photo_carrying(row)
    except ValueError:
        return None
    else:
        return Truck(row[BRAND], row[PHOTO], row[CARRYING], row[BODY_WHL])


def check_spec_mach(row):
    try:
        get_photo_carrying(row)
        if len(row[EXTRA]) == 0:
            raise ValueError
    except ValueError:
        return None
    else:
        return SpecMachine(row[BRAND], row[PHOTO], row[CARRYING], row[EXTRA])


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            if len(row) != 7:
                continue
            if row[CAR_TYPE] == 'car':
                car = check_car(row)
                if car:
                    car_list.append(car)
            elif row[CAR_TYPE] == 'truck':
                car = check_truck(row)
                if car:
                    car_list.append(car)
            elif row[CAR_TYPE] == 'spec_machine':
                car = check_spec_mach(row)
                if car:
                    car_list.append(car)
    return car_list

# print(get_car_list('_af3947bf3a1ba3333b0c891e7a8536fc_coursera_week3_cars.csv'))