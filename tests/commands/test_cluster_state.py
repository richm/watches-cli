"""Tests for our `watches cluster_state` subcommand."""


import json
from subprocess import PIPE, Popen as popen
from secure_support import TestSecureSupport
from watches.util import ESClientProducer


class TestClusterState(TestSecureSupport):
    def test_returns_json(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_state'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 9)

    def test_returns_cluster_state_local(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_state', '--local'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 9)

    def test_returns_cluster_state(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_state'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('state_uuid' in o)
        self.assertTrue('master_node' in o)
        self.assertTrue('nodes' in o)
        self.assertTrue('version' in o)
        self.assertTrue('blocks' in o)
        self.assertTrue('routing_table' in o)
        self.assertTrue('routing_nodes' in o)
        self.assertTrue('metadata' in o)

        metadata = o['metadata']
        self.assertTrue('cluster_uuid' in metadata)
        self.assertTrue('templates' in metadata)
        self.assertTrue('indices' in metadata)

    def test_returns_cluster_state_metric_and_index(self):
        es = ESClientProducer.create_client(
            self.options_from_list(self.appendSecurityCommands([]))
        )
        es.create(index='i', doc_type='t', id='1', body={}, ignore=409, refresh=True)

        cmd = self.appendSecurityCommands(['watches', 'cluster_state', '--metric=metadata', '--index=i'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 2)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('metadata' in o)
        self.assertTrue('i' in o['metadata']['indices'])

    def test_returns_cluster_state_filtered(self):
        cmd = self.appendSecurityCommands(['watches', 'cluster_state', '-f cluster_name', '-f master_node'])
        output = popen(cmd, stdout=PIPE).communicate()[0]
        o = json.loads(output)
        self.assertTrue(len(o) == 2)
        self.assertTrue('cluster_name' in o)
        self.assertTrue('master_node' in o)