import os, glob

figures_dir = 'papers/University_CSE_Thesis/figures'
all_figs = [
    'fig_benign_vs_smurfing_topology.pdf',
    'fig_1_3_failure_modes.pdf',
    'fig1_operational_architecture_flowchart.pdf',
    'fig21_adversarial_camouflage_topology.pdf',
    'fig_2_3_1wl_failure_vs_invariants.pdf',
    'fig_lit_evolution_frontier.pdf',
    'fig3_1_tensor_flow.pdf',
    'fig_canonical_invariants.pdf',
    'fig_12d_toy_model_schematic.pdf',
    'fig_triband_decay_comparison.pdf',
    'fig_triband_waveform_spectrum.pdf',
    'fig18_graphsmote_synthesis_pipeline.pdf',
    'fig_3_10_gradient_dynamics.pdf',
    'fig_algorithm1_flowchart.pdf',
    'fig_canonical_invariants_empirical.pdf',
    'fig22_triband_spectral_coldstart.pdf',
    'fig4_1_duckdb_arrow_pipeline.pdf',
    'fig4_2_database_erd.pdf',
    'fig_4_3_causal_slicing.pdf',
    'fig_operational_workflow.pdf',
    'fig19_conformal_risk_mechanism.pdf',
    'fig_conformal_conveyor_funnel.pdf',
    'fig_5_6_aci_drift_convergence.pdf',
    'fig4_conformal_queue_dynamics.pdf',
    'fig_5_7_fairness_audit.pdf',
    'fig_compliance_alert_funnel.pdf',
    'fig_forensic_swarm.pdf',
    'fig_ast_grammar_pipeline.pdf',
    'fig_15node_forensic_progression.pdf',
    'fig_single_alert_timeline.pdf',
    'fig_6_5_merkle_audit_tree.pdf',
    'fig_class_imbalance_log.pdf',
    'fig_temporal_split.pdf',
    'fig_champion_vs_runnerup_delta.pdf',
    'fig_critical_difference_lollipop.pdf',
    'fig7_multi_dataset_radar.pdf',
    'fig1_pr_roc_curves.pdf',
    'fig3_ablation_component_study.pdf',
    'fig_ablation_waterfall.pdf',
    'fig_leave_one_out_impact.pdf',
    'fig_invariant_importance_tornado.pdf',
    'fig9_adversarial_camouflage_robustness.pdf',
    'fig_edge_gate_distribution.pdf',
    'fig2_tsne_manifold_separation.pdf',
    'fig_zero_shot_transfer_heatmap.pdf',
    'fig_streaming_latency_waterfall.pdf',
    'fig_fastpath_latency_comparison.pdf',
    'fig_all_datasets_pr_curves.pdf',
    'fig_system_architecture.pdf',
    'fig8_2_uml_sequence_lifeline.pdf',
    'fig8_1_fastapi_k8s_topology.pdf',
    'fig_enterprise_deployment_lifecycle.pdf',
    'fig_regulatory_shields.pdf',
    'fig_9_3_multibank_split_gnn.pdf',
    'fig_hyperparam_sensitivity_4panel.pdf'
]

py_files = glob.glob('scripts/*.py')
mapping = {}

for fig in all_figs:
    stem = fig.replace('.pdf', '')
    found = []
    for py in py_files:
        with open(py, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if fig in content or f'"{stem}"' in content or f"'{stem}'" in content:
                found.append(os.path.basename(py))
    mapping[fig] = found

for fig, scripts in mapping.items():
    print(f"{fig} -> {scripts}")

