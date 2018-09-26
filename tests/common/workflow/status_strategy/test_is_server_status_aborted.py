# coding: utf-8
from nmp_broker.common.workflow.status_strategy import is_server_status_aborted


def test_ecflow_status():
    from nwpc_workflow_model.ecflow import NodeStatus
    assert is_server_status_aborted(NodeStatus.aborted)
    assert is_server_status_aborted(NodeStatus.aborted.value)
    assert is_server_status_aborted(NodeStatus.aborted.name.lower())


def test_sms_status():
    from nwpc_workflow_model.sms import NodeStatus
    assert is_server_status_aborted(NodeStatus.Aborted)
    assert is_server_status_aborted(NodeStatus.Aborted.value)
    assert is_server_status_aborted(NodeStatus.Aborted.name.lower())


def test_string_status(app):
    assert is_server_status_aborted('abo')
    assert is_server_status_aborted('aborted')
