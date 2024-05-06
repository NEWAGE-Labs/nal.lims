from bika.lims import api
from nal.lims import api.bad as bad
import math

def calculate(sample):
	#Catch bad input
	if sample is None or not hasattr(sample,'portal_type'):
		raise("Invalid object to calculate. Object does not exist or does not have a type.\nObject: {}".format(sample))
	elif sample.portal_type != 'AnalysisRequest':
		raise("Invalid object to calculate. Object exists but is not an AnalysisRequest.\nObject Type is: {}".format(sample.portal_type))

	analyses = []
	analyses_with_results = []
	calc_analyses = []
	for analysis in map(api.get_object,sample.getAnalyses())
		if api.get_workflow_status_of(analysis) not in bad:
			analyses.append(analysis)
			if analysis.Result is not None and analysis.Result != '':
				analyses_with_results.append(analysis)
			if analysis.getCalculation() is not None:
				calc_analyses.append(analysis)

	if len(calc_analyses) == 0 or len(analyses_with_results) == 0:
		return None

	try:
		keywords_with_results = {a.Keyword:float(a.Result) for a in analyses_with_results}
	except ValueError:
		raise("Cannot convert one of these results to a float: {}".format([a.Result for a in analyses_with_results]))

	import __future__

	calculated = []
	for test in calc_analyses:
		formula = test.getCalculation().getFormula()
		test_keywords = parse_keywords(formula)
		if not set(test_keywords).issubset(set(keywords_with_results.keys())):
			pass
		else:
			details = process_formula(test, formula, test_keywords, analyses_with_results)
			result = eval(compile(details['formula'], '<string>', 'eval',__future__.division.compiler_flag))
			test.Result = unicode(result)
			test.Method = details['method']
			test.AnalysisDateTime = details['datetime']
			calculated.append(test)

	return calculated

def parse_keywords(formula):
	if not isinstance(formula, str):
		raise("Invalid formula. Formula is not a string")

	keywords = []
	psplit = formula.split('[')[1:]
	for i in psplit:
		keywords.append(i.split(']')[0])
	return keywords

def process_formula(test, formula, keyword_dict, analyses):
	if not isinstance(formula, str):
		raise("Invalid formula. Formula is not a string")

	formula = formula.replace('[','').replace(']','')
	details = {}

	for keyword in keyword_dict.keys():
		analysis = [a for a in analyses if keyword == a.Keyword][0]
		result = float(analysis.Result)
		formula.replace(keyword,keyword_dict[keyword])

	from DateTime import DateTime

	details['formula'] = formula
	details['datetime'] = DateTime().Date()
	details['method'] = [j.UID() for j in map(api.get_object_by_uid,[i['methodid'] for i in test.getAnalysisService().MethodRecords])][0]

	return details
