class Car:
    def __init__(self, city, manufacture, model, year, fuel, gear, wd, doors, seats, car_class, reg_number, price, about, photo_path=None):
        self.city = city
        self.manufacture = manufacture
        self.model = model
        self.year = year
        self.fuel = fuel
        self.gear = gear
        self.wd = wd
        self.doors = doors
        self.seats = seats
        self.car_class = car_class
        self.reg_number = reg_number
        self.price = price
        self.about = about
        self.photo_path = photo_path

    def __repr__(self):
        photo_status = "Present" if self.photo_path else "None"
        return (f"Car(city={self.city}, make={self.manufacture}, model={self.model}, "
                f"year={self.year}, reg={self.reg_number}, photo={photo_status})")