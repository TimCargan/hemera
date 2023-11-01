import mlflow
import os
from absl import flags
from flax.traverse_util import flatten_dict

from hemera.standard_logger import logging

FLAGS = flags.FLAGS


def ml_flow_track(f=None, /, *, expr_name, version):
    experiment = mlflow.get_experiment_by_name(expr_name)
    if not experiment:
        mlflow.create_experiment(expr_name)
    mlflow.set_experiment(expr_name)

    def wrap(f):
        def new_main(*args, **kwargs):
            # config = FLAGS.config
            flag_dict = {k: {x.name: x.value for x in v} for k, v in list(FLAGS.flags_by_module_dict().items())}
            with mlflow.start_run(run_id=FLAGS.run_id) as run:
                logging.info("run_id: %s", run.info.run_id)

                if not FLAGS.run_id:
                    # Log params if a new exper
                    # TODO: else restore flag values?
                    config_flat_dict = {".".join(k).replace("/", "."): v for k, v in flatten_dict(flag_dict).items()}
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
