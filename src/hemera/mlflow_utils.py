import mlflow
import os
from absl import flags
from flax.traverse_util import flatten_dict

from hemera.path_translator import get_path
from hemera.standard_logger import logging

FLAGS = flags.FLAGS


def ml_flow_track(f=None, /, *, expr_name, version):

    art_base = get_path("mlflow")
    mlflow.set_tracking_uri(f"sqlite:///{art_base}/tracking.sqlite")
    experiment = mlflow.get_experiment_by_name(expr_name)
    if not experiment:
        art_base = os.path.join(art_base, "runs")
        mlflow.create_experiment(expr_name, artifact_location=art_base)
    mlflow.set_experiment(expr_name)

    def wrap(f):
        def new_main(*args, **kwargs):
            # config = FLAGS.config
            with mlflow.start_run(run_id=FLAGS.run_id) as run:
                logging.info("run_id: %s", run.info.run_id)

                if not FLAGS.run_id:
                    # Log params if a new exper
                    # TODO: else restore flag values?
                    config_flat_dict = {".".join(k): v for k, v in flatten_dict(FLAGS.to_dict()).items()}
                    mlflow.log_params(config_flat_dict)
                    # FLAG TAGS?
                    mlflow.set_tag("Version", version)
                    mlflow.set_tag("SLURM_ID", os.environ.get("SLURM_JOB_ID", "0"))
                f(*args, **kwargs)
        return new_main

    # See if we're being called as @ml_flow_track or @ml_flow_track().
    if f is None:
        # We're called with parens.
        return wrap

    # We're called as @ml_flow_track without parens.
    return wrap(f)
