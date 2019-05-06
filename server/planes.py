
class plan:
    def __init__(self, price = 0, voice = 0, sms = 0, data = 0):
        self.price, self.voice, self.sms, self.data = price, voice, sms, data


planes = [
    plan(7.0, data = 600),
    plan(10, data = 1024),
    plan(20, data = 2560),
    plan(30, data = 4096),
    plan(1.5, voice = 5),
    plan(2.9, voice = 10),
    plan(4.2, voice = 15),
    plan(6.5, voice = 25),
    plan(10.0, voice = 40),
    plan(0.7, sms = 10),
    plan(1.3, sms = 20),
    plan(2.1, sms = 35),
    plan(2.5, sms = 45) #,

    #plan(6.0, voice = 20, sms = 30, data = 100),
    #plan(10.0, voice = 30, data = 150),
    #plan(3.0, sms = 10, data = 100),
    #plan(8.0, voice = 15, data = 800),
    #plan(20.0, voice = 30, sms = 40, data = 3000),
    #plan(14.0, voice = 50, sms = 80)
]
