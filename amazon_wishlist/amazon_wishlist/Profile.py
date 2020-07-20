class Profile:
    def __init__(self,name,price,site):
        self.name=name
        self.price=price
        self.site=site
        self.lowest=price
        self.avg=price