from airflow.models import DagBag
import pytest
import os
import json

class TestSanityOfDag():
    #Apply appropriate load time for your workflows
    EXPECTED_LOAD_TIME = 0.5
    
    def setUp(self):
        self.dagbag = DagBag(os.path.expanduser("/usr/local/airflow/dags"), include_examples=False)

    def test_import_dags(self):
        assert (len(self.dagbag.import_errors)) == 0, 'DAG failed with import errors : {}'.format(
                self.dagbag.import_errors
            )

    def test_parse_time(self):
        metric = self.dagbag.dagbag_stats
        for o in metric:
            assert (o.duration.seconds) <= self.EXPECTED_LOAD_TIME, '{file} take {actual_load_time}s and is more than {expected_load_time}s: '.format(
                expected_load_time=self.EXPECTED_LOAD_TIME,
                actual_load_time=o.duration,
                file=o.file[1:]
            )
