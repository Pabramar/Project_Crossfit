import datetime

dt_tomorrow=datetime.date.today() + datetime.timedelta(days=1)
print(dt_tomorrow)

dt= str(dt_tomorrow)
def convert_format(s: str):
    y, d, m = s.split("-")
    return "-".join((m, d, y))

algo=convert_format(dt)
print(algo) # D-M-Y for link address


