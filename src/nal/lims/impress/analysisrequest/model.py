# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.IMPRESS.
#
# SENAITE.IMPRESS is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2023 by it's authors.
# Some rights reserved, see README and LICENSE.

import itertools

from bika.lims.utils import format_supsub
from bika.lims.utils import formatDecimalMark
from bika.lims.utils import to_utf8
from bika.lims.utils.analysis import format_uncertainty
from bika.lims import api
from senaite.app.supermodel import SuperModel as BaseModel
from senaite.impress import logger
from senaite.impress.decorators import returns_super_model
from math import floor
from math import log10
import re

class SuperModel(BaseModel):
    """Analysis Request SuperModel
    """

#Start Custom Methods
    def get_loq(self, analysis):
        analysis = api.get_object(analysis)
        #If Override is set, use Override as LOQ
        if hasattr(analysis,'LOQOverride') and analysis.LOQOverride is not None and analysis.LOQOverride != '':
            try:
                loq = float(analysis.LOQOverride)
                return loq
            except:
                pass

        #Get Custom Method for base LOQ
	method = api.get_object_by_uid(analysis.CustomMethod)
	if method is not None:
            print("Method for {}-{} is {} UID: {}".format(api.get_id(self),analysis.title,method, method.UID()))
	else:
	    raise Exception("{} for sample {} does not have an assigned Method".format(analysis.title, api.get_id(self)))
        loq = None
        for i in analysis.getAnalysisService().MethodRecords:
            if i['methodid'] == method.UID():
                if i['loq'] == 'P|A':
                    return 'P|A'
                print("loq for {} is: {}".format(api.get_object(analysis),i['loq']))
                loq = float(i['loq'])
                if hasattr(analysis,'Dilution') and analysis.Dilution is not None:
                    try:
                       loq = loq*float(analysis.Dilution)
                    except:
                        raise Exception("Dilution for {} is not a valid float - {}".format(analysis.title, analysis.Dilution))
                #If the LOQ Multiplier is set, multiply the LOQ by 10
                if hasattr(analysis,'LOQMultiplier') and analysis.LOQMultiplier is True:
                    loq = loq*10
        if loq is None:
            raise Exception("LOQ not set for {} with method {}".format(analysis.title,method))
	return loq

    def get_cf(self):
        weight = None
        volume = None
        for i in map(api.get_object,self.getAnalyses()):
            if api.get_workflow_status_of(i) not in ['cancelled','retracted','rejected','invalid']:
                if i.Keyword == 'weight':
                    weight = i
                elif i.Keyword == 'volume':
                    volume = i
        if weight is None or volume is None:
            return 1
        else:
            try:
                w = float(weight.Result)
                v = float(volume.Result)
            except ValueError as ve:
                raise("Problem calculating correction factor from Weight and Volume. Please enter valid values.")
            return v/w

    def getAnalysisByKey(self, keyword):
	for i in map(api.get_object,self.getAnalyses()):
	    if i.Keyword == keyword and api.get_workflow_status_of(i) not in ['cancelled','invalid','rejected','retracted']:
		return i

    def getCRA(self):
	model = self
	CRA_ans = []
	for i in model.getAnalyses():
	    analysis = api.get_object(i)
	    print(analysis)
	    for j in ['arsenic','antimony','cadmium','chromium','copper','lead','mercury','nickel']:
		if j in analysis.Keyword:
		    CRA_ans.append(analysis)
	def sort_func(a):
	    return api.get_title(a).lower()
	CRA_ans.sort(key=sort_func)
	return tuple(CRA_ans)

    def getPairType(self):
        """
        :return: Returns a string of how to identify the sample type on a report
        :rtype: String
        """
        types = {
            'NewSap':'New',
            'OldSap':'Old',
            'Root':'Root',
            #Waters
        }
        stype = self.getSampleType().title
        if stype == 'Sap':
            if self.NewLeaf:
                stype = 'New'+stype
            else:
                stype = 'Old'+stype

        return types[stype]

    def getPairRGB(self):
        """
        :return: Returns a 3-element RGB Tuple
        :rtype: Tuple
        """
        colors = {
            'NewSap':(100,212,70),
            'OldSap':(46,99,29),
            'Root':(150,75,0),
        }
        stype = self.getSampleType().title
        if stype == 'Sap':
            if self.NewLeaf:
                stype = 'New'+stype
            else:
                stype = 'Old'+stype

        return colors[stype]


    def getSampleComments(self):
    	list_of_text = self.ResultsInterpretationDepts
    	if list_of_text:
    	    text_with_html = list_of_text[0]['richtext']
    	else:
    	    return ''
    	headtags = re.compile('<.?>')
    	text2 = re.sub(headtags,'',text_with_html)
    	tailtags = re.compile('</.?>')
    	text3 = re.sub(tailtags,'',text2)
    	linefeeds = re.compile('&nbsp;')
    	text4 = re.sub(linefeeds,'',text3)
    	return text4

    def isRoot(self):
        return self.getSampleType().title == 'Root'

    def hasLeadCopper(self):
       if 'Lead/Copper - Drinking Water' in [i.title for i in self.getProfiles()]:
           return True
       else:
           return False

    def get_nitrogen_conversion_effeciency(self):
        total_n = 0
        no3 = 0
        nh4 = 0
        ncr = ''
	logger.warn("Starting {}".format(self))
        found = False
        for i in range(20, 0, -1):
            if found==False:
                version = 'nitrogen-'+str(i)
                if hasattr(self,version):
                    found = True
		    try:
                    	total_n = float(self[version].Result)
		    except ValueError as ve:
			total_n = 'NT'
        if found == False and hasattr(self,'nitrogen'):
	    try:
                total_n = float(self.nitrogen.Result)
	    except ValueError as ve:
		no3 = 'NT'

        found = False
        for i in range(20, 0, -1):
            if found==False:
                version = 'nitrogen_nitrate-'+str(i)
                if hasattr(self,version):
                    found = True
		    try:
                    	no3 = float(self[version].Result)
		    except ValueError as ve:
			no3 = 'NT'
        if found == False and hasattr(self,'nitrogen_nitrate'):
	    try:
                no3 = float(self.nitrogen_nitrate.Result)
	    except ValueError as ve:
		no3 = 'NT'

        found = False
        for i in range(20, 0, -1):
            if found==False:
                version = 'nitrogen_ammonium-'+str(i)
                if hasattr(self,version):
                    found = True
		    try:
                    	nh4 = float(self[version].Result)
		    except ValueError as ve:
			nh4 = 'NT'
        if found == False and hasattr(self,'nitrogen_ammonium'):
	    try:
                nh4 = float(self.nitrogen_ammonium.Result)
	    except ValueError as ve:
		nh4 = 'NT'

	logger.warn("NO3 for {} is: {}".format(self, no3))
        if total_n == 0 or total_n == 'NT' or no3 == 'NT' or nh4 == 'NT':
            ncr = 'NT'
	    print("{} is 'NT'".format(self))
        elif total_n < 0.01:
            ncr = '-'
        else:
            if total_n == '':
                total_n = 0
            if nh4 == '' or nh4 < 0:
                nh4 = 0
            if no3 == '' or no3 < 0:
                no3 = 0
            ncr = float(1 - ((nh4 + no3)/total_n))*100
            ncr = round(ncr, 3-int(floor(log10(abs(ncr))))-1)

        return ncr

    def get_project_contact(self):
        batch = api.get_object(self.getBatch())
        project_contact = batch.getReferences(relationship="SDGProjectContact")
	if len(project_contact) > 0:
	    project_contact = project_contact[0]
	else:
	    project_contact = api.get_object_by_uid(batch.ProjectContact)
        project_contact_name = project_contact.Firstname + " " + project_contact.Surname
        return project_contact_name

    def get_sampler_contact(self):
        batch = api.get_object(self.getBatch())
        project_contact = batch.getReferences(relationship="SDGSamplerContact")
	if len(project_contact) > 0:
	    project_contact = project_contact[0]
	else:
	    project_contact = api.get_object_by_uid(batch.SamplerContact)
        project_contact_name = project_contact.Firstname + " " + project_contact.Surname
        return project_contact_name

    def get_grower_contact(self):
        batch = api.get_object(self.getBatch())
        project_contact = batch.getReferences(relationship="SDGGrowerContact")
	if len(project_contact) > 0:
	    project_contact = project_contact[0]
	else:
	    project_contact = api.get_object_by_uid(batch.GrowerContact)
        project_contact_name = ''
        if project_contact:
            project_contact_name = project_contact.Firstname + " " + project_contact.Surname
        return project_contact_name

    def get_attachment_file(self):
        attachment = self.Attachment[0]
        return attachment

    def get_attachment_files(self):
        attachments = []
        for i in self.Attachment:
            attachments.append(i)
        return attachments

    def get_analyst_initials(self, analysis):
        return analysis.getAnalystInitials()

    def get_optimal_high_level(self, keyword):
        max = ''
        for i in self.getResultsRange():
            if i['keyword'] ==  keyword:
                max = i.get('max', '')
        return max

    def get_optimal_low_level(self, keyword):
        min = ''
        for i in self.getResultsRange():
            if i['keyword'] ==  keyword:
                min = i.get('min', '')
        return min

    def get_result_bar_percentage(self, keyword, rperc=False):

        specs = ''
        for i in self.getResultsRange():
            if i['keyword'] ==  keyword:
                specs = i

        perc = 0
	result_str = ''
	ldl = 0.01
	if 'nitrogen' in keyword:
	    ldl = 0.01
	else:
	    ldl = 0.05
        if specs:
            found = False
            for i in range(10, 0, -1):
                if found==False:
                    version = keyword+'-'+str(i)
                    if hasattr(self,version):
                        found = True
                        result_str = str(self[version].Result).strip()
            if found == False and hasattr(self,keyword):
                result_str = str(self[keyword].Result).strip()

            min_str = str(specs.get('min', 0)).strip()
            max_str = str(specs.get('max', 99999)).strip()
            min = -1
            max = -1
            result = -1

            try:
                min = float(min_str)
            except ValueError:
                pass
            try:
                max = float(max_str)
            except ValueError:
                pass
            try:
                result = float(result_str)
            except ValueError:
                pass

            if result < ldl:
                result = 0
	    if min == 0:
		min = 0.01
            if min != -1 and max != -1 and result != -1 and max != 0:
		if rperc:
		    result = result*.0001
                if result <= min:
                    perc = (result/min)*(100/3)
                elif result >= max:
                    perc = (200/3) + ((100/3)-(100/3)/(result/max))
                else:
                    perc = (100/3) + (((result-min)/(max-min))*(100/3))
        return perc

    def get_report_result(self, analysis, digits, pflag=False, corr = 1):
	"""Return formatted result or NT
        """
	analysis = api.get_object(analysis)
        result = analysis.getResult()
        choices = analysis.getResultOptions()
	sample = analysis.aq_parent

        if choices:
            # Create a dict for easy mapping of result options
            values_texts = dict(map(
                lambda c: (str(c["ResultValue"]), c["ResultText"]), choices
            ))

            # Result might contain a single result option
            match = values_texts.get(str(result))
            if match:
                return match

        if analysis is None or result == "":
            return "NT"
        dil = 1
	print("Result is: {}".format(result))
	result = float(result)*float(corr)

	#Get Custom Method
	method = api.get_object_by_uid(analysis.CustomMethod)
	if method is not None:
            print("Method for {}-{} is {}".format(api.get_id(sample),analysis.title,method))
	else:
	    raise Exception("{} for sample {} does not have an assigned Method".format(analysis.title, api.get_id(sample)))

	#Get Dilution if it exists
        if hasattr(analysis,'Dilution') and analysis.Dilution is not None and analysis.Dilution != '':
	    print("Dilution is: {}".format(analysis.Dilution))
	    dil = float(analysis.Dilution)

        if analysis.getAnalysisService().getCategory().title == "Microbiology":
	    print("Result is: {}".format(result))
	    uloq = ''
	    for i in analysis.getAnalysisService().MethodRecords:
		print("Method comp is: {} : {}".format(i['methodid'],method.UID()))
		if i['methodid'] == method.UID():
		    print("uloq is: {}".format(i['uloq']))
		    uloq = i['uloq']
	    if result == 0:
                return '< {}'.format(dil)
	    if result >= 1 and result <= float(uloq):
		if 'c18' not in analysis.Keyword or dil > 1:
		    xresult = round(result*dil, digits-int(floor(log10(abs(result*dil))))-1)
		else:
		    xresult = result
		if int(xresult) == xresult:
		    return int(xresult)
		else:
		    return xresult
	    if result > float(uloq):
		return '> {}'.format(float(uloq)*dil)
        else:
            loq = self.get_loq(analysis)
            if loq == '':
		raise Exception("LOQ not set for {} with method {}".format(analysis.title,method))
	    elif result < loq:
		    return '< {}'.format(loq*dil)
            else:
		if pflag:
		    result = result*0.0001
		xresult = round((result*dil), digits-int(floor(log10(abs(result*dil))))-1)
		if int(xresult) == xresult:
		    return int(xresult)
		else:
		    return xresult
	return result

    def get_received_date(self):
        """Returns the batch date formatted as [Month Day, Year]
        """
        batch = api.get_object(self.getBatch())
        try:
            received_date = batch.SDGDate.strftime("%b %d, %Y")
            return received_date or ""
        except TypeError:
            raise TypeError("No SDG Recieved Date")
#End Custom Methods

    def is_invalid(self):
        return self.isInvalid()

    def is_provisional(self):
        if self.is_invalid():
            return True
        valid_states = ['verified', 'published']
        return api.get_review_status(self.instance) not in valid_states

    def is_out_of_range(self, analysis):
        """Check if the analysis is out of range
        """
        from bika.lims.api.analysis import is_out_of_range
        return is_out_of_range(analysis.instance)[0]

    def is_retest(self, analysis):
        """Check if the analysis is a retest
        """
        return analysis.isRetest()

    def get_workflow_by_id(self, wfid):
        """Returns a workflow by ID

        :returns: DCWorkflowDefinition instance
        """
        wf_tool = api.get_tool("portal_workflow")
        return wf_tool.getWorkflowById(wfid)

    def get_transitions(self):
        """Return possible transitions
        """
        wf_tool = api.get_tool("portal_workflow")
        return wf_tool.getTransitionsFor(self.instance)

    def get_workflow_history(self, wfid, reverse=True):
        """Return the (reversed) review history
        """
        wf_tool = api.get_tool("portal_workflow")
        history = wf_tool.getHistoryOf(wfid, self.instance)
        if reverse:
            return history[::-1]
        return history

    def get_workflow_info_for(self, wfid):
        """Return a workflow info object
        """
        workflow = self.get_workflow_by_id(wfid)
        # the state variable, e.g. review_state
        state_var = workflow.state_var
        # tuple of possible transitions
        transitions = self.get_transitions()
        # review history tuple, e.g. ({'action': 'publish', ...}, )
        history = self.get_workflow_history(wfid)
        # the most current history info
        current_state = history[0]
        # extracted status id
        status = current_state[state_var]
        # `StateDefinition` instance
        state_definition = workflow.states[status]
        # status title, e.g. "Published"
        status_title = state_definition.title
        # return selected workflow information for the wrapped instance
        return {
            "id": wfid,
            "status": status,
            "status_title": status_title,
            "state_var": state_var,
            "transitions": transitions,
            "review_history": history,
        }

    def get_transition_date(self, wfid, state):
        """Return the date when the transition was made
        """
        wf = self.get_workflow_info_for(wfid)

        for rh in wf.get("review_history"):
            if rh.get("review_state") == state:
                return rh.get("time")
        return None

    @property
    def scientific_notation(self):
        setup = api.get_setup()
        return int(setup.getScientificNotationReport())

    @property
    def decimal_mark(self):
        return self.aq_parent.getDecimalMark()

    def get_formatted_unit(self, analysis):
        """Return formatted Unit
        """
        return format_supsub(to_utf8(analysis.Unit))

    def get_formatted_result(self, analysis):
        """Return formatted result
        """
        return analysis.getFormattedResult(
            specs=analysis.getResultsRange(),
            sciformat=self.scientific_notation,
            decimalmark=self.decimal_mark)

    def get_formatted_uncertainty(self, analysis):
        uncertainty = format_uncertainty(
            analysis.instance,
            decimalmark=self.decimal_mark,
            sciformat=self.scientific_notation)
        return "[&plusmn; {}]".format(uncertainty)

    def get_formatted_specs(self, analysis):
        specs = analysis.getResultsRange()
        fs = ''
        if specs.get('min', None) and specs.get('max', None):
            fs = '%s - %s' % (specs['min'], specs['max'])
        elif specs.get('min', None):
            fs = '> %s' % specs['min']
        elif specs.get('max', None):
            fs = '< %s' % specs['max']
        return formatDecimalMark(fs, self.decimal_mark)

    def get_resultsinterpretation(self):
        ri_by_depts = self.ResultsInterpretationDepts

        out = []
        for ri in ri_by_depts:
            dept = ri.get("uid", "")
            title = getattr(dept, "title", "")
            richtext = ri.get("richtext", "")
            out.append({"title": title, "richtext": richtext})

        return out

    def get_sorted_attachments(self, option="r"):
        """Return the sorted AR/AN Attachments with the given Report Option set
        """
        ar_attachments = self.Attachment
        an_attachments = [a for a in itertools.chain(*map(
            lambda an: an.Attachment, self.Analyses))]
        attachments = filter(lambda a: a.getReportOption() == option,
                             ar_attachments + an_attachments)
        return self.sort_attachments(attachments)

    def get_sorted_ar_attachments(self, option="r"):
        """Return the sorted AR Attchments with the given Report Option set
        """
        # AR attachments in the correct order
        attachments = self.sort_attachments(self.Attachment)
        # Return filtered list by report option
        return filter(lambda a: a.getReportOption() == option, attachments)

    def get_sorted_an_attachments(self, option="r"):
        """Return the sorted AN Attchments with the given Report Option set
        """
        attachments = []
        for analysis in self.Analyses:
            for attachment in self.sort_attachments(analysis.Attachment):
                if attachment.getReportOption() != option:
                    continue
                # Append a tuples of analysis, attachment
                attachments.append((analysis, attachment))
        return attachments

    def sort_attachments(self, attachments=[]):
        """Attachment sorter
        """
        inf = float("inf")
        view = self.restrictedTraverse("attachments_view")
        order = view.get_attachments_order()

        def att_cmp(att1, att2):
            _n1 = att1.UID()
            _n2 = att2.UID()
            _i1 = _n1 in order and order.index(_n1) + 1 or inf
            _i2 = _n2 in order and order.index(_n2) + 1 or inf
            return cmp(_i1, _i2)

        return sorted(attachments, cmp=att_cmp)

    @property
    @returns_super_model
    def departments(self):
        return self.getDepartments()

    @property
    def managers(self):
        out = []
        for dept in self.departments:
            manager = dept.Manager
            if not manager:
                continue
            if manager in out:
                continue
            out.append(manager)
        return out

    @property
    def verifiers(self):
        """Returns a list of user objects
        """
        out = []
        # extract the ids of the verifiers from all analyses
        userids = [analysis.getVerificators() for analysis in self.Analyses]
        # flatten the list
        userids = list(itertools.chain.from_iterable(userids))
        # get the users
        for userid in set(userids):
            if not userid:
                continue
            user = api.get_user(userid)
            if user is None:
                logger.warn("Could not find user '{}'".format(userid))
                continue
            out.append(user)
        return out
