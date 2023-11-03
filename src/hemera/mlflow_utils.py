import mlflow
import os
from absl import flags
from flax.traverse_util import flatten_dict
from typing import Optional

from hemera.standard_logger import logging

flags.DEFINE_string("expr_name", None, "MlFlow Experiment Name")
flags.DEFINE_string("run_id", default=None, help="MlFlow run_id, if set will restart the run")
flags.DEFINE_string("run_name", default=None, help="MlFlow run display name")
flags.DEFINE_list("module_filter", default=["absl", "tensorflow", "chex"], help="List of modules to filter out of logging")
FLAGS = flags.FLAGS


def ml_flow_track(f=None, /, *, expr_name: Optional[str] = None, **out_kwargs):
    """Decorator to run MLFlow tracking.

    :param f: Function to wrap
    :param expr_name: The experiment name, Note: this is overwritten by FLAG.exper_name
    :param kwargs: A KV dict of dict[str,str] of tags to log for the experimet
    :return:
    """
    def wrap(f):
        def new_main(*args, **kwargs):
            # Set the exper name
            _expr_name = FLAGS.get_flag_value("expr_name", expr_name) # Use flag if set otherwise value passed in
            experiment = mlflow.get_experiment_by_name(_expr_name)
            if not experiment:
                mlflow.create_experiment(expr_name)
            mlflow.set_experiment(expr_name)

            with mlflow.start_run(run_id=FLAGS.run_id, run_name=FLAGS.run_name) as run:
                logging.info("run_id: %s", run.info.run_id)

                if not FLAGS.run_id:
                    # Log params if a new exper
                    # TODO: else restore flag values?
                    # TODO: Better way than logging all flag values
                    # config = FLAGS.config
                    flag_dict = {k: {x.name: x.value for x in v} for k, v in list(FLAGS.flags_by_module_dict().items())}
                    # Filter out modules
                    flag_dict = {k: v for k, v in flag_dict.items() if not any([k.startswith(m) for m in FLAGS.module_filter])}
                    config_flat_dict = {".".join(k).replace("/", "."): v for k, v in flatten_dict(flag_dict).items()}
                    mlflow.log_params(config_flat_dict)

                    # Log Tags
                    for k, v in out_kwargs.items():
                        mlflow.set_tag(k, v)
                    mlflow.set_tag("SLURM_ID", os.environ.get("SLURM_JOB_ID", "0"))
                f(*args, **kwargs)

        return new_main

    # See if we're being called as @ml_flow_track or @ml_flow_track().
    if f is None:
        # We're called with parens.
        return wrap

    # We're called as @ml_flow_track without parens.
    return wrap(f)
