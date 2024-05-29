import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
import pandas as pd
from nal.lims import api as napi
from math import floor
from math import log10
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection

BAD = ['rejected','retracted','invalid','cancelled']

def check_pair(pair):
    if len(pair) == 1:
        pair = pair[0]
        return pair
    elif len(pair) > 1:
        IStatusMessage(self.request).addStatusMessage(
            u"Unexpected Behavior. Are there multiple SubGroups with the same number?",
            'warning'
        )
        self.request.response.redirect(api.get_url(self.context))
    elif len(pair) == 0:
        IStatusMessage(self.request).addStatusMessage(
            u"Unexpected Behavior. Are there enough SubGroups to handle this many pairs?",
            'warning'
        )
        self.request.response.redirect(api.get_url(self.context))

class AddPairsView(BrowserView):

    def __init__(self, context, request):
        alsoProvides(request, IDisableCSRFProtection)
        self.context = context
        self.request = request

    def __call__(self):

        sdg = self.context
        all_ars = map(api.get_object,sdg.getAnalysisRequests())
        ars = [ar for ar in all_ars if api.get_workflow_status_of(ar) not in BAD]
        ardict = {}
        for ar in ars:
            ardict[int(api.get_id(ar)[1:])] = ar

        for ar in ars:
            for an in map(api.get_object,ar.getAnalyses()):
                if api.get_workflow_status_of(an) not in BAD and an.Result is not None and an.Result != '':
                    print("Result for {} is {}".format(ar.id,an.Result))
                    IStatusMessage(self.request).addStatusMessage(
                        u"Incomplete. Analyses already have results.",
                        'warning'
                    )
                    self.request.response.redirect(api.get_url(self.context))
                    return None

        sorted_dict = dict(sorted(ardict.items()))
        print("sorted dict: {}".format(sorted_dict))
        for key,value in sorted_dict.items():
            print("ID: {}".format(key))
        new = True
        subgroup = 1
        subgroups = map(api.get_object,api.search({'portal_type':'SubGroup'}))
        count = 0
        for key, value in sorted_dict.items():
            pair = [sg for sg in subgroups if str(subgroup).zfill(2) in sg.title]
            pair = check_pair(pair)
            value.setSubGroup(pair)
            value.reindexObject(idxs=['SubGroup'])
            if value.getBatch() is not None:
                value.getBatch().reindexObject()
            count += 1
            if new:
                new = False
            else:
                new = True
                subgroup += 1

        IStatusMessage(self.request).addStatusMessage(
                u"Successfully added {} Pairs".format(count)
            )

        self.request.response.redirect(api.get_url(self.context))

class AddNewOldView(BrowserView):

    def __init__(self, context, request):
        alsoProvides(request, IDisableCSRFProtection)
        self.context = context
        self.request = request

    def __call__(self):

        sdg = self.context
        all_ars = map(api.get_object,sdg.getAnalysisRequests())
        ars = [ar for ar in all_ars if api.get_workflow_status_of(ar) not in BAD]
        ardict = {}
        for ar in ars:
            ardict[int(api.get_id(ar)[1:])] = ar

        for ar in ars:
            for an in map(api.get_object,ar.getAnalyses()):
                if api.get_workflow_status_of(an) not in BAD and an.Result is not None and an.Result != '':
                    print("Result for {} is {}".format(ar.id,an.Result))
                    IStatusMessage(self.request).addStatusMessage(
                        u"Incomplete. Analyses already have results.",
                        'warning'
                    )
                    self.request.response.redirect(api.get_url(self.context))
                    return None

        sorted_dict = dict(sorted(ardict.items()))
        print("sorted dict: {}".format(sorted_dict))
        for key,value in sorted_dict.items():
            print("ID: {}".format(key))
        new = True
        count = 0
        for key, value in sorted_dict.items():
            value.NewLeaf = new
            value.reindexObject(idxs=['NewLeaf'])
            count += 1
            if new:
                new = False
            else:
                new = True

        IStatusMessage(self.request).addStatusMessage(
                u"Successfully added 'New Leaf' to batch"
            )

        self.request.response.redirect(api.get_url(self.context))


class AddILIView(BrowserView):

    def __init__(self, context, request):
        alsoProvides(request, IDisableCSRFProtection)
        self.context = context
        self.request = request

    def __call__(self):

        sdg = self.context
        all_ars = map(api.get_object,sdg.getAnalysisRequests())
        ars = [ar for ar in all_ars if api.get_workflow_status_of(ar) not in BAD]
        ardict = {}
        for ar in ars:
            ardict[int(api.get_id(ar)[1:])] = ar

        for ar in ars:
            for an in map(api.get_object,ar.getAnalyses()):
                if api.get_workflow_status_of(an) not in BAD and an.Result is not None and an.Result != '':
                    print("Result for {} is {}".format(ar.id,an.Result))
                    IStatusMessage(self.request).addStatusMessage(
                        u"Incomplete. Analyses already have results.",
                        'warning'
                    )
                    self.request.response.redirect(api.get_url(self.context))
                    return None

        sorted_dict = dict(sorted(ardict.items()))
        print("sorted dict: {}".format(sorted_dict))
        for key,value in sorted_dict.items():
            print("ID: {}".format(key))
        ili = 1
        for key, value in sorted_dict.items():
            value.InternalLabID = str(ili).zfill(3)
            value.reindexObject(idxs=['InternalLabID'])
            ili += 1

        IStatusMessage(self.request).addStatusMessage(
                u"Successfully added 'Internal Lab IDs' to batch"
            )

        self.request.response.redirect(api.get_url(self.context))

class AddFullPairsView(BrowserView):

    def __init__(self, context, request):
        alsoProvides(request, IDisableCSRFProtection)
        self.context = context
        self.request = request

    def __call__(self):

        sdg = self.context
        all_ars = map(api.get_object,sdg.getAnalysisRequests())
        ars = [ar for ar in all_ars if api.get_workflow_status_of(ar) not in BAD]
        ardict = {}
        for ar in ars:
            ardict[int(api.get_id(ar)[1:])] = ar

        for ar in ars:
            for an in map(api.get_object,ar.getAnalyses()):
                if api.get_workflow_status_of(an) not in BAD and an.Result is not None and an.Result != '':
                    print("Result for {} is {}".format(ar.id,an.Result))
                    IStatusMessage(self.request).addStatusMessage(
                        u"Incomplete. Analyses already have results.",
                        'warning'
                    )
                    self.request.response.redirect(api.get_url(self.context))
                    return None

        sorted_dict = dict(sorted(ardict.items()))
        new = True
        subgroup = 1
        subgroups = map(api.get_object,api.search({'portal_type':'SubGroup'}))
        count = 0
        for key, value in sorted_dict.items():
            pair = [sg for sg in subgroups if str(subgroup).zfill(2) in sg.title]
            pair = check_pair(pair)
            value.setSubGroup(pair)
            value.NewLeaf = new
            value.reindexObject(idxs=['SubGroup'])
            if value.getBatch() is not None:
                value.getBatch().reindexObject()
            count += 1
            if new:
                new = False
            else:
                new = True
                subgroup += 1

        IStatusMessage(self.request).addStatusMessage(
                u"Successfully added {} Pairs with New/Old Flagging".format(count)
            )

        self.request.response.redirect(api.get_url(self.context))
