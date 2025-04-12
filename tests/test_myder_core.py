import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

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
    assert "SampleProvider: running with model=test-model" in captured.outdef test_openrouter_provider_properties():
    from provider.openrouter import OpenRouterProvider
    provider = OpenRouterProvider(api_key="dummy-key")
    assert provider.name == "openrouter"
    assert provider.base_url == "https://openrouter.ai/api/v1"
    assert provider.api_key == "dummy-key"

def test_run_openrouter_provider():
    from myder_core import run_provider
    result = run_provider("openrouter", api_key="dummy-key", model="gpt-3.5")
    assert "Provider: openrouter" in result
    assert "API Key: dummy-key" in result
    assert "Model: gpt-3.5" in result
