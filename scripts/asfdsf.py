from datetime import datetime

dt_now = datetime.now()
dt = str(datetime.date(dt_now))

def convert_format(s: str):
    y, d, m = s.split("-")
    return "-".join((m, d, y))

algo=convert_format(dt)
print(algo) # D-M-Y for link address


