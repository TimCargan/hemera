import os
from json import JSONDecodeError
from pathlib import Path
from unittest.mock import MagicMock, patch
from absl import flags
from absl.testing import parameterized, absltest, flagsaver

FLAGS = flags.FLAGS


class test_path_translater(parameterized.TestCase):

    @parameterized.parameters(("data", Path('/ML/data')),
                              ("mlflow", Path('/ML/mlflow')))
    @patch.dict(os.environ, {"HEMERA_PATHS": "../data/good_path_data.json"})
    def test_good_get_path(self, test, true):
        from hemera.path_translator import get_path
        data_path = get_path(test)
        self.assertEqual(data_path, true)

    @patch.dict(os.environ, {"HEMERA_PATHS": "../data/bad_json.json"})
    def test_get_path_bad_json(self):
        with self.assertRaises(JSONDecodeError):
            from hemera.path_translator import get_path

    @absltest.skip("Can't hook into logger so can't test")
    @patch.dict(os.environ, {"HEMERA_PATHS": "../data/non_existent_json.json"})
    def test_log_no_file(self):
        with self.assertLogs() as cm:
            from hemera.path_translator import get_path
            self.assertEqual(["No path dict found at: %s"], cm.output)
