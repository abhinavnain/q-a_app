import os, csv, datetime
from .db.configurator import Raas


def dictify(data, columns=[""]):
    return [{ col:row[idx] for idx, col in enumerate(columns)} for row in data]


def get_tenant(uri):
    return Raas(uri.split("-")[0].split("//")[1],os.getenv("env_name"))

#ts_utc = datetime.datetime.utcnow
def ts_utc(add_minutes=0):
    ts = datetime.datetime.utcnow()
    if add_minutes>=0:
        return ts+datetime.timedelta(minutes=add_minutes)
    else:
        return ts-datetime.timedelta(minutes=add_minutes)

ts_ist = lambda: ts_utc(add_minutes=330)
ts_wform = lambda ts,form: ts.strftime(form)
ts_str = lambda ts: ts.strftime("%y-%m-%d.%H-%M-%S")
oi_format = "%y%m%d%H%M%S"
create_orchestration_identifier = lambda: ts_ist().strftime(oi_format)
get_ts_from_oi = lambda oi: datetime.datetime.strptime(oi, oi_format)


rcsv        = lambda fi, enc: list(csv.reader(open(fi,'rt',newline='',encoding = enc), delimiter=','))
rcsv_utf    = lambda fi: rcsv(fi,'utf8')
rcsv_latin1 = lambda fi: rcsv(fi, 'latin1')
rcsv_cp35   = lambda fi: rcsv(fi, 'cp35')
wcsv        = lambda fi, dat, enc: csv.writer(open(fi,'w',newline='',encoding = enc)).writerows(dat)
wcsv_utf    = lambda fi, dat: wcsv(fi, dat,'utf8')
wcsv_latin1 = lambda fi, dat: wcsv(fi, dat,'latin1')
wcsv_cp35   = lambda fi, dat: wcsv(fi, dat,'cp35')
acsv        = lambda fi, dat, enc: csv.writer(open(fi,'a',newline='',encoding = enc)).writerows(dat)
acsv_utf    = lambda fi, dat: acsv(fi, dat,'utf8')
acsv_latin1 = lambda fi, dat: acsv(fi, dat,'latin1')
acsv_cp35   = lambda fi, dat: acsv(fi, dat,'cp35')