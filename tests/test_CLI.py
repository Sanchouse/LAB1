import subprocess

class TestCLI:
    def test_cli_expression(self):
        result = subprocess.run(
            ["python", "-m", "toolkit", "calc", "2+2"],
            capture_output=True,
            text=True,
            cwd="src"
        )

        assert result.returncode == 0

    def test_cli_calc_help(self):
        result = subprocess.run(
            ["python", "-m", "toolkit", "calc", "--help"],
            capture_output=True,
            text=True,
            cwd="src"
        )

        assert result.returncode == 0

    def test_cli_help(self):
        result = subprocess.run(
            ["python", "-m", "toolkit", "--help"],
            capture_output=True,
            text=True,
            cwd="src"
        )

        assert result.returncode == 0

    def test_cli_calc_error(self):
        result = subprocess.run(
            ["python", "-m", "toolkit", "calc", ""],
            capture_output=True,
            text=True,
            cwd="src"
        )

        assert result.returncode == 2

    def test_cli_convert_error(self):
        result = subprocess.run(
            ["python", "-m", "toolkit", "convert", "1.5", "--from", "km", "--to", "kg"],
            capture_output=True,
            text=True,
            cwd="src"
        )

        assert result.returncode == 2

    def test_cli_empty(self):
        result = subprocess.run(
            ["python", "-m", "toolkit"],
            capture_output=True,
            text=True,
            cwd="src"
        )

        assert result.returncode == 2