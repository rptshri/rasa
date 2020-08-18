import os
from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch
from _pytest.pytester import Testdir


def test_plugins(testdir: Testdir, monkeypatch: MonkeyPatch, tmp_path: Path):
    expected_output = "Hello Rasa plugin"
    plugin_script = f"""#!/bin/bash
echo "{expected_output}"
    """
    script_path = tmp_path / "rasa-hello"
    script_path.write_text(plugin_script)
    script_path.chmod(0o777)

    monkeypatch.setenv("PATH", f"{os.getenv('PATH')}:{str(tmp_path)}")

    result = testdir.run("rasa", "hello")
    assert result.ret == 0
    assert result.outlines[0] == expected_output


def test_plugin_with_script_error(
    testdir: Testdir, monkeypatch: MonkeyPatch, tmp_path: Path
):
    plugin_script = f"""#!/bin/basdadssh
echo "bla"
    """
    script_path = tmp_path / "rasa-hello"
    script_path.write_text(plugin_script)
    script_path.chmod(0o777)

    monkeypatch.setenv("PATH", f"{os.getenv('PATH')}:{str(tmp_path)}")

    result = testdir.run("rasa", "hello")
    assert result.ret == 1

    assert any("No such file or directory" in line for line in result.errlines)
