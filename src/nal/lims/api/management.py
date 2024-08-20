import pandas as pd
from bika.lims import api
from DateTime import DateTime

mgmt_dir = '/mnt/Data/Lab Management Exports/Overdue Accounts/'

def get_samples_by_week(weeks_back=1):
	ARs = api.search({'portal_type':'AnalysisRequest'})
	recentARs = [api.get_object(ar) for ar in ARs if ar.getBatchUID is not None and DateTime(api.get_object_by_uid(ar.getBatchUID).SDGDate).year() == DateTime().year() and int(DateTime(api.get_object_by_uid(ar.getBatchUID).SDGDate).month()) > int((DateTime().month())-2)]
        wk = int(DateTime().week()) - weeks_back
        newARs = []
	for ar in recentARs:
		if int(DateTime(ar.getBatch().SDGDate).week()) == wk:
			newARs.append(ar)

	ids = []
	sdgs = []
	dates = []
	for i in newARs:
		ids.append(api.get_id(i))
		sdgs.append(i.getBatch().title)
		dates.append(DateTime.strftime(i.getBatch().SDGDate, format="%m/%d/%Y"))

	dfdict = {'id':ids,'SDG':sdgs,'received':dates}
	df = pd.DataFrame(dfdict)
	df.to_csv('/mnt/Data/Lab Management Exports/Sample Count by Week/Week {} - Received {} Samples.csv'.format(wk, df['id'].count()))


def get_sample_counts_by_year_and_week():
	return

def get_intake():
	return

def get_overdue_clients():
	clients = map(api.get_object,api.search({'portal_type':'Client'}))
	overdue = {}
	overdue['NAL Number'] = []
	overdue['Name'] = []

	for client in clients:
		if hasattr(client, 'Overdue') and client.Overdue:
			overdue['NAL Number'] = client.ClientID
			overdue['Name'] = client.Name

	df = pd.DataFrame(overdue)
	df.to_csv('/mnt/Data/Lab Management Exports/Overdue Accounts/{}.csv'.format(DateTime.day()))
