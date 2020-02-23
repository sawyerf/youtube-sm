from time import localtime
from datetime import datetime, timedelta

def lcl_time(day=31, all_time=False):
	if all_time:
		return 0
	return int(since(day))

def since(day):
	date	= datetime.now() - timedelta(days=day)
	return date.strftime("%Y%m%d000000")
	
