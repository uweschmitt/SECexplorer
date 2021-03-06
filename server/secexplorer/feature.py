#encoding: utf-8
from __future__ import absolute_import

from rpy2 import robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects import numpy2ri

import sys

base = importr('base')
print >> sys.stderr, base.R_home()
print >> sys.stderr, base._libPaths()

pandas2ri.activate()
numpy2ri.activate()

robjects.numpy2ri.activate()

secprofiler = importr('SECprofiler')


def get_protein_traces_by_id(protein_ids, id_type):
    result = secprofiler.runSECexplorer(protein_ids, id_type)
    traces = pandas2ri.ri2py_dataframe(result[1][0][0])
    traces = traces.set_index(["id"])
    traces.index.name = "protein_id"
    return traces


def _compute_complex_features(protein_ids, id_type):
    traces = get_protein_traces_by_id(protein_ids, id_type)
    result = secprofiler.findComplexFeatures(traces, traces.index, 0.99)
    features = pandas2ri.ri2py(result[1])
    print(features)
    features['n_subunits'] = [len(r) for r in features.subgroup.str.split(';')]
    features_dicts = []
    for idx, row in features.iterrows():
        print >> sys.stderr, row
        features_dicts.append(row.to_dict())
    return features_dicts


def compute_complex_features(protein_ids, id_type):
    result = secprofiler.runSECexplorer(protein_ids, id_type)

    features = pandas2ri.ri2py_dataframe(result[1][1])
    # traces = pandas2ri.ri2py_dataframe(result[1][0][0])
    # traces = traces.set_index(["id"])
    # traces.index.name = "protein_id"

    left_pp = features.left_pp   # war: Start SEC
    right_pp = features.right_pp   # war: End SEC
    apex = features.apex
    number_of_subunits = features.n_subunits_detected  # #subunits spalte
    number_of_subunits = features.n_subunits_detected  # #subunits spalte
    cluster_score = features.sw_score  # cluster_score spalte
    intensity_based_stoc = features.stoichiometry_estimated
    complex_mw_estimated = features.complex_mw_estimated
    #complex_sec_estimated
    #complex_sec_estimated

    """
    gui: choose uniprotkb, uniprotkb_name, gene_names, ensembl, hgnc
    gui: felder für fehler

    x gui: plotte left / right boundaries / apex
    x gui: highlight color of activated row
    x gui: traces plotten
    """

    failed_conversion = pandas2ri.ri2py_listvector(result[0][0])
    no_ms_signal = pandas2ri.ri2py_listvector(result[0][1])
    successfull = pandas2ri.ri2py_listvector(result[0][2])
    mapping_table = pandas2ri.ri2py_listvector(result[0][3])

    features['n_subunits'] = [len(r) for r in features.subunits_detected.str.split(';')]
    features_dicts = []
    for idx, row in features.iterrows():
        features_dicts.append(row.to_dict())
    return features_dicts

