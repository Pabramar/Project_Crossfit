import datetime
import re
import sys

def create_logs():
    f = open("test.log","w+")
    f.write("**************************\n")
    f.write("TEST LOG               ***\n")
    f.write("**************************\n")
    f.close()
    
create_logs()

#----------------------------------------------------
def get_crossfit_web_date():
    today_date=datetime.date.ctime(datetime.date.today())
    print(today_date) # Here we get the type of day that is

    if re.search("^Mon*", today_date):
        print("It's Monday")
        date_class=str(datetime.date.today() + datetime.timedelta(days=1))
        
    elif re.search("^Tue*", today_date):
        print("It's Tuesday")
        date_class=str(datetime.date.today() + datetime.timedelta(days=2))
        
    else: 
        with open("test.log", "a+") as myfile:
            myfile.write("[ERROR] Not executed on monday or tuesday\n")
        sys.exit("[ERROR] Not executed on monday or tuesday\n")
        
    crossfit_date_web=_convert_format(date_class)
    LOG.info(f"Date used for web url:{crossfit_date_web}") # D-M-Y for link address
    return crossfit_date_web
#----------------------------------------------------
      
def _convert_format(s: str):
    y, d, m = s.split("-")
    return "-".join((m, d, y))

crossfit_date_web=_convert_format(date_class)
print(crossfit_date_web) # D-M-Y for link address


