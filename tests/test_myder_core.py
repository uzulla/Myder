import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import pytest
import myder_core

def test_list_providers():
    providers = myder_core.list_providers()
    assert "sample_provider" in providers

def test_load_provider():
    provider = myder_core.load_provider("sample_provider")
    assert hasattr(provider, "run")

def test_run_provider(capsys):
    myder_core.run_provider("sample_provider", model="test-model")
    captured = capsys.readouterr()
    assert "SampleProvider: running with model=test-model" in captured.out