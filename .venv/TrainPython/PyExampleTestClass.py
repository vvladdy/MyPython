class Car:

    def __init__(self, brand, model, year, color):
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.total_drive_km = 0

    def repaint(self, color):
        self.color = color

    def drive(self, km_drive):
        self.total_drive_km += km_drive

    def __repr__(self):
        return (self.brand + ',' + self.model + ',' + str(self.year) + '' +
                self.color)

    def __str__(self):
        return (self.brand + ',' + self.model + ',' + str(self.year))


class Truck(Car):

    def __init__(self, brand, model, year, color, tralers):
        super().__init__(brand, model, year, color)
        self.tralers = tralers

    def attach_traler(self, num_traler=1):
        self.tralers += num_traler

    def detach_traler(self, num_traler=1):
        self.tralers -= num_traler

    def __repr__(self):
        return (self.brand + ',' + self.model + ',' + str(self.year) + '' +
                self.color + ' ' +  self.tralers)

model = Car('Subary', 'Impresa', 2008, 'red')
model.repaint('blue')
print(model.color)

