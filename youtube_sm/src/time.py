from time import localtime

def lcl_time(nb_month=1, all_time=False):
	if all_time:
		return 0
	tps = localtime()
	tm_year, tm_mon, tm_mday = tps.tm_year, tps.tm_mon, tps.tm_mday
	if tm_mon <= nb_month:
		if nb_month >= 12:
			tm_year -= int(nb_month/12)
			tm_mon -= (nb_month % 12)
		else:
			tm_mon = 12 + (tm_mon - nb_month)
			tm_year -= 1
	else:
		tm_mon -= nb_month
	return split_to_date(tm_year, tm_mon, tm_mday)

def since(day):
	tps = localtime()
	tm_year, tm_mon, tm_mday = tps.tm_year, tps.tm_mon, tps.tm_mday
	if day >= 365: #year(s)
		var = (day-(day%365))
		tm_year -= var/365
		day -= var
	if day >= 31: #month(s)
		var = (day-(day%31))
		tm_mon = tm_mon - var/31
		if tm_mon <= 0:
			tm_year -= 1
			tm_mon += 12
		day -= var
	if day >= 0: #week(s)
		tm_mday -= day
		if tm_mday <= 0:
			tm_mday += 31
			tm_mon -= 1
			if tm_mon <= 0:
				tm_year -= 1
				tm_mon += 12
		return split_to_date(tm_year, tm_mon, tm_mday, False)
	
def split_to_date(tm_year, tm_mon, tm_mday, nb=True):
	tm_mday = str(tm_mday)[:2]
	tm_mon = str(tm_mon)[:2].replace('.', '')
	tm_year = str(tm_year)[:4]
	if len(tm_mday) == 1:
		tm_mday = '0' + tm_mday
	if len(tm_mon) == 1:
		tm_mon = '0' + tm_mon
	if nb:
		return int(tm_year + tm_mon + tm_mday + '000000')
	else:
		return tm_year + tm_mon + tm_mday + '000000'