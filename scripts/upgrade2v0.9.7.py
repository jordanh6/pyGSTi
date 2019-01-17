from __future__ import print_function
import sys, re, shutil, os

def build_regex(repls):
    regex_els = []
    for k in repls.keys():
        if k.startswith('.'):
            regex_els.append( "%s\\b" % re.escape(k) )
        elif k.endswith('_'):
            regex_els.append( "\\b%s" % re.escape(k) )
        else:
            regex_els.append( "\\b%s\\b" % re.escape(k) )
    regex_str = "|".join(regex_els)
    regex = re.compile(regex_str)
    return regex

def multiple_replace(regex, repls, text): 
    def fn(matchObj):
        return repls[matchObj.group(0)]
    return regex.sub(fn, text)

def main(argv):
    if len(argv) < 1+1:
        print(("This script upgrades scripts or notebooks written for "
               "pyGSTi version 0.9.6 and lower to use pyGSTi v0.9.7. "
               "It's not guaranteed to work perfectly in all cases, but "
               "it should get you most of the way there."))
        print("Usage: <filename1> <filename2> ...")
        return
      
    regex = build_regex(replacements)
    filecnt = 0
    
    for filename in argv[1:]:
        if filename == __file__: continue # don't process this file
        if filename.endswith(".bak"): continue # don't process .bak files

        if os.path.exists(filename + ".bak"): # don't overwrite .bak files
            backup_str = "(using existing " + filename + ".bak as source)"
        else:
            shutil.copyfile(filename, filename + ".bak") #make backup copy
            backup_str = "( backup " + filename + ".bak created)"

        infilename = filename + ".bak"
        outfilename = filename

        print("Processing %s %s" % (outfilename,backup_str))
        with open(infilename,'r') as infile:
            fileText = infile.read()
        finalText = multiple_replace(regex, replacements,fileText)
        with open(outfilename,'w') as outfile:
            outfile.write(finalText)
        filecnt += 1

    print("Finished!  Made replacements in %d files." % filecnt)
    return


replacements = {
"list_all_gatestrings_without_powers_and_cycles" : "list_all_circuits_without_powers_and_cycles",
"gateset_with_lgst_gatestring_estimates" : "model_with_lgst_circuit_estimates",
"is_gatestring_allowed_by_exclusion" : "is_circuit_allowed_by_exclusion",
"is_gatestring_allowed_by_inclusion" : "is_circuit_allowed_by_inclusion",
"GateSetGOtoTargetVarSpamVecArray" : "ModelGOtoTargetVarSpamVecArray",
"indices_sorted_by_gatestring_len" : "indices_sorted_by_circuit_len",
"gateStringSetsToUseInEstimation" : "circuitSetsToUseInEstimation",
"listOfGateLabelTuplesOrStrings" : "listOfOpLabelTuplesOrStrings",
"compiled_gatestring_spamTuples" : "compiled_circuit_spamTuples",
"list_random_gatestrings_onelen" : "list_random_circuits_onelen",
"listOfGateLabelTuplesOrString" : "listOfOpLabelTuplesOrString",
"build_nqubit_standard_gateset" : "build_standard_localnoise_model",
"LindbladParameterizedGateMap" : "LindbladOp",
"gateStringsToUseInEstimation" : "circuitsToUseInEstimation",
"gatestring_color_scatterplot" : "circuit_color_scatterplot",
"LindbladParameterizedSPAMVec" : "LindbladSPAMVec",
"LindbladParameterizedPOVM" : "LindbladPOVM",
"EigenvalueParameterizedGate" : "EigenvalueParamDenseOp",
"list_all_gatestrings_onelen" : "list_all_circuits_onelen",
"find_closest_unitary_gatemx" : "find_closest_unitary_opmx",
"manipulate_gatestring_list" : "manipulate_circuit_list",
"gen_all_gatestrings_onelen" : "gen_all_circuits_onelen",
"build_nqn_noncomposed_gate" : "build_nqn_noncomposed_op",
"gatestring_color_histogram" : "circuit_color_histogram",
"LindbladParameterizedGate" : "LindbladDenseOp",
"LinearlyParameterizedGate" : "LinearlyParamDenseOp",
"translate_gatestring_list" : "translate_circuit_list",
"merge_gate_and_noop_bases" : "merge_op_and_noop_bases",
"compress_gate_label_tuple" : "compress_op_label_tuple",
"gate_from_error_generator" : "operation_from_error_generator",
"FullyParameterizedSPAMVec" : "FullSPAMVec",
"generate_gatestring_list" : "generate_circuit_list",
"compiled_gatestring_list" : "compiled_circuit_list",
"gatestring_color_boxplot" : "circuit_color_boxplot",
"gatematrix_color_boxplot" : "opmatrix_color_boxplot",
"create_random_gatestring" : "create_random_circuit",
"vectorized_gate_el_index" : "vectorized_op_el_index",
"clifford_gates_on_qubits" : "clifford_ops_on_qubits",
"CPTPParameterizedSPAMVec" : "CPTPSPAMVec",
"targetGateFilenameOrSet" : "targetModelFilenameOrObj",
"listOfGateStringsToKeep" : "listOfCircuitsToKeep",
"nparams_nqnoise_gateset" : "nparams_XYCNOT_cloudnoise_model",
"make_bootstrap_gatesets" : "make_bootstrap_models",
"expand_gate_label_tuple" : "expand_op_label_tuple",
"evaluate_gatefn_by_name" : "evaluate_opfn_by_name",
"gateset_to_group_labels" : "model_to_group_labels",
"focused_mc2gst_gatesets" : "focused_mc2gst_models",
"create_nqubit_sequences" : "create_standard_cloudnoise_sequences",
"modelGateFilenameOrSet" : "modelFilenameOrObj",
"FullyParameterizedGate" : "FullDenseOp",
"create_gatestring_list" : "create_circuit_list",
"gauge_optimize_gs_list" : "gauge_optimize_model_list",
"info_of_gatefn_by_name" : "info_of_opfn_by_name",
"direct_mc2gst_gatesets" : "direct_mc2gst_models",
"focused_mc2gst_gateset" : "focused_mc2gst_model",
"gatestringconstruction" : "circuitconstruction",
"TPParameterizedSPAMVec" : "TPSPAMVec",
"gatestringWeightsDict" : "circuitWeightsDict",
"gateStringsToEstimate" : "circuitsToEstimate",
"GateGaugeGroupElement" : "OpGaugeGroupElement",
"nestedGateStringLists" : "nestedCircuitLists",
"manipulate_gatestring" : "manipulate_circuit",
"list_lgst_gatestrings" : "list_lgst_circuits",
"build_nqnoise_gateset" : "build_standard_cloudnoise_model",
"write_gatestring_list" : "write_circuit_list",
"direct_mc2gst_gateset" : "direct_mc2gst_model",
"direct_mlgst_gatesets" : "direct_mlgst_models",
"gateLabelsToEstimate" : "opLabelsToEstimate",
"guessGatesetForGauge" : "guessModelForGauge",
"directMLEGSTgatesets" : "directMLEGSTmodels",
"focusedLSGSTgatesets" : "focusedLSGSTmodels",
"gatesetFilenameOrObj" : "modelFilenameOrObj",
"CompressedGateString" : "CompressedCircuit",
"gateStringToEstimate" : "circuitToEstimate",
"translate_gatestring" : "translate_circuit",
"process_gate_strings" : "process_circuits",
"list_all_gatestrings" : "list_all_circuits",
"build_nqubit_gateset" : "build_standard_localnoise_model",
"load_gatestring_list" : "load_circuit_list",
"gatestring_structure" : "circuit_structure",
"resolved_gatestrings" : "resolved_circuits",
"compressedGateString" : "compressedCircuit",
"tree_gatestring_list" : "tree_circuit_list",
"germsVsGatesetScores" : "germsVsModelScores",
"randomizeGatesetList" : "randomize_model_list",
"direct_lgst_gatesets" : "direct_lgst_models",
"direct_mlgst_gateset" : "direct_mlgst_model",
"gatestring_list_lbl" : "circuit_list_lbl",
"directLSGSTgatesets" : "directLSGSTmodels",
"TPParameterizedGate" : "TPDenseOp",
"GatestringStructure" : "CircuitStructure",
"DMGateCRep_Lindblad" : "DMOpCRep_Lindblad",
"SBGateCRep_Embedded" : "SBOpCRep_Embedded",
"SVGateCRep_Embedded" : "SVOpCRep_Embedded",
"DMGateCRep_Embedded" : "DMOpCRep_Embedded",
"SBGateCRep_Composed" : "SBOpCRep_Composed",
"SVGateCRep_Composed" : "SVOpCRep_Composed",
"DMGateCRep_Composed" : "DMOpCRep_Composed",
"SBGateCRep_Clifford" : "SBOpCRep_Clifford",
"GatestringPlaquette" : "CircuitPlaquette",
"_WeightedGateString" : "_WeightedOpString",
"gateStringSetLabels" : "circuitSetLabels",
"maxGateStringLength" : "maxCircuitLength",
"filter_gate_strings" : "filter_op_strings",
"make_qutrit_gateset" : "make_qutrit_model",
"gen_all_gatestrings" : "gen_all_circuits",
"basis_build_gateset" : "basis_build_explicit_model",
"build_alias_gateset" : "build_explicit_alias_model",
"compile_gatestrings" : "compile_circuits",
"LGSTcompatibleGates" : "LGSTcompatibleOps",
"compiled_gatestring" : "compiled_circuit",
"gatestring_compiler" : "circuit_compiler",
"direct_lgst_gateset" : "direct_lgst_model",
"gatesetconstruction" : "modelconstruction",
"gatestring_structs" : "circuit_structs",
"from_gateset_label" : "from_model_label",
"includeTargetGates" : "includeTargetOps",
"directLGSTgatesets" : "directLGSTmodels",
"GateTermCalculator" : "TermForwardSimulator",
"DMGateRep_Lindblad" : "DMOpRep_Lindblad",
"SBGateRep_Embedded" : "SBOpRep_Embedded",
"SVGateRep_Embedded" : "SVOpRep_Embedded",
"DMGateRep_Embedded" : "DMOpRep_Embedded",
"SBGateRep_Composed" : "SBOpRep_Composed",
"SVGateRep_Composed" : "SVOpRep_Composed",
"DMGateRep_Composed" : "DMOpRep_Composed",
"SBGateRep_Clifford" : "SBOpRep_Clifford",
"objects.gatestring" : "objects.circuit",
"compile_gatestring" : "compile_circuit",
"dsGateStringsToUse" : "dsCircuitsToUse",
"filter_gatestrings" : "filter_circuits",
"embed_gate_unitary" : "embed_operator_unitary",
"gate_count_nparams" : "op_count_nparams",
"gate_intrinsic_err" : "op_intrinsic_err",
"idt_idle_gatelabel" : "idt_idle_oplabel",
"indexforGatestring" : "indexforCircuit",
"setup_gateset_list" : "setup_model_list",
"get_gateset_params" : "get_model_params",
"reducedGatesetList" : "reducedModelList",
"flattened_gate_dim" : "flattened_op_dim",
"tupleOfGateLabels" : "tupleOfOpLabels",
"gatestringWeights" : "circuitWeights",
"gatestrings_label" : "circuits_label",
"directGSTgatesets" : "directGSTmodels",
"DMGateCRep_Sparse" : "DMOpCRep_Sparse",
"import gatestring" : "import circuit",
"gateStringIndices" : "circuitIndices",
"filter_gatestring" : "filter_circuit",
"decomp_gate_index" : "decomp_op_index",
"insert_gate_basis" : "insert_op_basis",
"get_start_gateset" : "get_start_model",
"gatesetfn_factory" : "modelfn_factory",
"gateLabelOrString" : "opLabelOrString",
"gate_error_labels" : "op_error_labels",
"gateLabelAliases" : "opLabelAliases",
"gatestring_lists" : "circuit_lists",
"to_gateset_label" : "to_model_label",
"gatesetOrDataset" : "modelOrDataset",
"GateStringParser" : "CircuitParser",
"TPInstrumentGate" : "TPInstrumentOp",
"DMGateRep_Sparse" : "DMOpRep_Sparse",
"SVGateCRep_Dense" : "SVOpCRep_Dense",
"DMGateCRep_Dense" : "DMOpCRep_Dense",
"finalGateStrings" : "finalCircuits",
"split_gatestring" : "split_circuit",
"gateStringsToUse" : "circuitsToUse",
"init_gatestrings" : "init_circuits",
"parse_gatestring" : "parse_circuit",
"basis_build_gate" : "basis_build_operation",
"from_gate_matrix" : "from_operation_matrix",
"factor_gate_reps" : "factor_op_reps",
"gates_to_compose" : "ops_to_compose",
"LindbladGateType" : "LindbladOpType",
"pgate_local_inds" : "paramop_local_inds",
"revGateLabelList" : "revOpLabelList",
"dgate_dgateLabel" : "dop_dopLabel",
"uniqueGateLabels" : "uniqueOpLabels",
"gateTargetLabels" : "opTargetLabels",
"gatelabel_filter" : "oplabel_filter",
"group_to_gateset" : "group_to_model",
"clifford_gateset" : "clifford_model",
"gateMxInStdBasis" : "opMxInStdBasis",
"group_or_gateset" : "group_or_model",
"gateInFinalBasis" : "opInFinalBasis",
"std1Q_XYI.gates" : "std1Q_XYI.gates",
"gateLabelString" : "opLabelString",
"targetGateLabel" : "targetOpLabel",
"gateStringLabel" : "circuitLabel",
"curStartGateset" : "curStartModel",
"gsStdevVecGates" : "mdlStdevVecOps",
"GateStringLexer" : "CircuitLexer",
"ComposedGateMap" : "ComposedOp",
"EmbeddedGateMap" : "EmbeddedOp",
"GateSetFunction" : "ModelFunction",
"SVGateRep_Dense" : "SVOpRep_Dense",
"DMGateRep_Dense" : "DMOpRep_Dense",
"gateStringLists" : "circuitLists",
"gateStringTuple" : "circuitTuple",
"gatestring_list" : "circuit_list",
"gatesfn_factory" : "opsfn_factory",
"gateExpressions" : "opExpressions",
"unreliableGates" : "unreliableOps",
"gate_exclusions" : "op_exclusions",
"gate_inclusions" : "op_inclusions",
"gate_wrtFilter1" : "op_wrtFilter1",
"gate_wrtFilter2" : "op_wrtFilter2",
"gatesOnlyString" : "opsOnlyString",
"gatesetByYthenX" : "modelByYthenX",
"target_gate_inv" : "target_op_inv",
"vec_gateset_dim" : "vec_model_dim",
"gateLabelTuple" : "opLabelTuple",
"gatelabel_list" : "oplabel_list",
"targetGatesets" : "targetModels",
"gatesetsByIter" : "modeslByIter",
"nearby_gateset" : "nearby_model",
"directGatesets" : "directModels",
"GateMatrixCalc" : "MatrixForwardSimulator",
"GateCalculator" : "ForwardSimulator",
"SBGateCRep_Sum" : "SBOpCRep_Sum",
"SVGateCRep_Sum" : "SVOpCRep_Sum",
"DMGateCRep_Sum" : "DMOpCRep_Sum",
"GateGaugeGroup" : "OpGaugeGroup",
"obj.gatestring" : "obj.circuit",
"gatestringList" : "circuitList",
"gateStringIndx" : "circuitIndx",
"nGatesetParams" : "nModelParams",
"iFlattenedGate" : "iFlattenedOp",
"gatefn_factory" : "opfn_factory",
"gateInStdBasis" : "opInStdBasis",
"compiled_gates" : "compiled_ops",
"raw_gatestring" : "raw_circuit",
"existing_gates" : "existing_ops",
"gateToOptimize" : "opToOptimize",
"gate_wrtFilter" : "op_wrtFilter",
"max_gate_noise" : "max_op_noise",
"errgen_gaterep" : "errgen_oprep",
"gate_term_reps" : "op_term_reps",
"closestUGateMx" : "closestUOpMx",
"gatestringlist" : "circuitlist",
"effective_gate" : "effective_op",
"reducedGateset" : "reducedModel",
"gatematrixcalc" : "matrixforwardsim",
"gateset_label" : "model_label",
"targetGateset" : "targetModel",
"targetGateSet" : "targetMDL",
"lsgstGatesets" : "lsgstModels",
"elgstGatesets" : "elgstModels",
"gs_primitives" : "mdl_primitives",
"SBGateRep_Sum" : "SBOpRep_Sum",
"SVGateRep_Sum" : "SVOpRep_Sum",
"DMGateRep_Sum" : "DMOpRep_Sum",
"GateSetMember" : "ModelMember",
"build_gateset" : "build_explicit_model",
"write_gateset" : "write_model",
"from_gate_obj" : "from_operation_obj",
"optimize_gate" : "optimize_operation",
"embedded_gate" : "embedded_op",
"compile_gates" : "compile_operations",
"gate_outcomes" : "op_outcomes",
"trans_gatestr" : "trans_opstr",
"virtual_gates" : "virtual_ops",
"dsGateStrings" : "dsCircuits",
"to_gatestring" : "to_circuit",
"possiblegates" : "possibleops",
"gatesetmember" : "modelmember",
"gateLabelSrc" : "opLabelSrc",
"startGateset" : "startModel",
"lsgstGateset" : "lsgstModel",
"elgstGateset" : "elgstModel",
"mleGateset_p" : "mleModel_p",
"idle_gateset" : "idle_model",
"inputGateset" : "inputModel",
"inputGateSet" : "inputModel",
"otherGateSet" : "otherModel",
"base_gateset" : "base_model",
"GateTermCalc" : "TermForwardSimulator",
"ComposedGate" : "ComposedDenseOp",
"EmbeddedGate" : "EmbeddedDenseOp",
"CliffordGate" : "CliffordOp",
"GateSetChild" : "ModelChild",
"gateStrTuple" : "opStrTuple",
"load_gateset" : "load_model",
"read_gateset" : "read_model",
"get_spamgate" : "get_spamop",
"factor_gates" : "factor_ops",
"composedGate" : "composedOp",
"gatetermcalc" : "termforwardsim",
"fastgatecalc" : "fastopcalc",
"gate_labels" : "op_labels",
"gateset_lbl" : "model_lbl",
"lgstGateset" : "lgstModel",
"mleGatesets" : "mleModels",
"seedGateset" : "seedModel",
"ref_gateset" : "ref_model",
"GateMapCalc" : "MapForwardSimulator",
"gatestrings" : "circuits",
"gateStrings" : "cirCuits",
"gate_string" : "op_string",
"idleGateStr" : "idleOpStr",
"numGateSets" : "numModels",
"gate_lookup" : "operation_lookup",
"gatesToOmit" : "opsToOmit",
"gatePenalty" : "opPenalty",
"gate_matrix" : "op_matrix",
"target_gate" : "target_op",
"singleGates" : "singleOps",
"factorgates" : "factorops",
"param_gates" : "param_ops",
"idtIdleGate" : "idtIdleOp",
"gatesetTyps" : "modelTyps",
"gateMxBasis" : "opMxBasis",
"gatesetname" : "modelname",
"gatesetList" : "modelList",
"gateset_num" : "model_num",
"gatemapcalc" : "mapforwardsim",
"gateTuples" : "opTuples",
"gateLabels" : "opLabels",
"gatelabels" : "oplabels",
"gate_label" : "op_label",
"mleGateset" : "mleModel",
"newGateset" : "newModel",
"simGateset" : "simModel",
"gsStdevVec" : "mdlStdevVec",
"gatesetObj" : "modelObj",
"StaticGate" : "StaticDenseOp",
"GateMatrix" : "DenseOperator",
"DMGateCRep" : "DMOpCRep",
"SVGateCRep" : "SVOpCRep",
"SBGateCRep" : "SBOpCRep",
"GateString" : "Circuit",
"gatestring" : "circuit",
"gateString" : "circuit",
"gate_tuple" : "oplabel_tuple",
"build_gate" : "build_operation",
"embed_gate" : "embed_operation",
"self_gates" : "self_operations",
"iter_gates" : "iter_operations",
"gateWeight" : "opWeight",
"gateMatrix" : "opMatrix",
"targetGate" : "targetOp",
"gate_noise" : "op_noise",
"gatesetByX" : "modelByX",
"gate_deriv" : "op_deriv",
"gate_evals" : "op_evals",
"gate_evecs" : "op_evecs",
"Gatestring" : "Circuit",
"sparseGate" : "sparseOp",
"gatesetnum" : "modelnum",
"gateLabel" : "opLabel",
"gateTuple" : "opTuple",
"gatelabel" : "oplabel",
"gateBasis" : "opBasis",
".gs_target.copy()" : ".target_model()",
".gs_target" : ".target_model()",
"gs_target" : "target_model",
"DMGateRep" : "DMOpRep",
"SVGateRep" : "SVOpRep",
"SBGateRep" : "SBOpRep",
"gatesetFn" : "modelFn",
"gateScore" : "opScore",
"gatetools" : "optools",
"gatesets" : "models",
"gate_dim" : "op_dim",
"gateName" : "opName",
"qutritGS" : "qutritMDL",
"GateCalc" : "ForwardSimulator",
"GateCRep" : "OpCRep",
"gatereps" : "operationreps",
"fidGates" : "fidOps",
"gateExpr" : "opExpr",
"pre_gate" : "pre_op",
"gate_err" : "op_err",
"gateSize" : "opSize",
"randGate" : "randOp",
"new_gate" : "new_op",
"gatesetA" : "modelA",
"gatesetB" : "modelB",
"rel_gate" : "rel_op",
"gatelist" : "operationlist",
"gate_std" : "op_std",
"numGates" : "numOps",
"gatecalc" : "forwardsim",
"gateset" : "model",
"GateMap" : "MapOperator",
"GateRep" : "OpRep",
".gates" : ".operations",
"dgate" : "doperation",
"hgate" : "hoperation",
"Gate" : "LinearOperator"
}

if __name__ == "__main__":
    main(sys.argv)
