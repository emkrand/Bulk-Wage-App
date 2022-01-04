class Employer:
    def __init__(self, name, ein, mailing_address, city, state_code, zip_code):
        self.name = name
        self.ein = ein
        self.mailing_address = mailing_address
        self.city = city
        self.state_code = state_code
        self.zip_code = zip_code
        self.employees = []