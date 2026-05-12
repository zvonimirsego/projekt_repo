class Users:
    def __init__(self, email, first_name, last_name, password, is_admin=False):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin

    def makeReservation(self):
        pass

    def deleteReservation(self):
        pass

class Admin(Users):
    def __init__(self, email, first_name, last_name, password):
        super().__init__(email, first_name, last_name, password, is_admin=True)

    def addEquipment(self):
        pass

    def editEquipment(self):
        pass

    def deleteEquipment(self):
        pass

    def sendWarning(self):
        pass
    

class Equipment:
    def __init__(self, id_equipment, equipment_name, condition, available):
        self.id_equipment = id_equipment
        self.equipment_name = equipment_name
        self.condition = condition
        self.available = available

    def checkAvailability(self):
        pass


class Loan:
    def __init__(self, id_loan, id_user, id_equipment, starting_date, due_date, returned):
        self.id_loan = id_loan
        self.id_user = id_user
        self.id_equipment = id_equipment
        self.starting_date = starting_date
        self.due_date = due_date
        self.returned = returned