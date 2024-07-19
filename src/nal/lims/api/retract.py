
def retract_batches_by_keyword(xbatches, xkeywords):
    from bika.lims import api
    import transaction as t
    batches = map(api.get_object,api.search({'portal_type':'Batch','title':xbatches}))
    for batch in batches:
        for sample in map(api.get_object,batch.getAnalysisRequests()):
            for analysis in map(api.get_object,sample.getAnalyses()):
                if analysis.Keyword in xkeywords:
                    try:
                        api.do_transition_for(analysis,'retract')
                        analysis.reindexObject()
                        print("Retracted {} for sample {} of batch {}".format(anaylsis.Keyword,api.get_id(sample),batch.title))
                    except:
                        pass
    t.get().commit()



