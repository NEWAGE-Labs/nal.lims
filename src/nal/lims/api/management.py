import pandas as pd
from bika.lims import api
from DateTime import DateTime

def get_samples_by_week():
	ARs = api.search({'portal_type':'AnalysisRequest'})
	recentARs = [api.get_object(ar) for ar in ARs if ar.getBatchUID is not None and DateTime(api.get_object_by_uid(ar.getBatchUID).SDGDate).year() == DateTime().year() and int(DateTime(api.get_object_by_uid(ar.getBatchUID).SDGDate).month()) > int((DateTime().month())-2)]
        wk = int(DateTime().week()) - 1
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
