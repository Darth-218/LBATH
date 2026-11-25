# Experiment registry

Each experiment gets a stable ID of the form `E###-short-name`. The registry
records the research question, hypothesis, configuration, dataset version,
seeds, model versions, command, output paths, and decision.

A run is reproducible only if its configuration and artifacts are registered
before results are cited in the paper. Config drift invalidates the experiment.
