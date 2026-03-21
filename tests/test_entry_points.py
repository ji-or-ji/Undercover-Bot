import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run_cmd(cmd, cwd):
    env = os.environ.copy()
    env["SKIP_LOGIN"] = "1"
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

def test_run_as_script():
    code, out, err = run_cmd([sys.executable, "src/bot/main.py"], ROOT)
    assert code == 0

def test_run_as_module():
    code, out, err = run_cmd([sys.executable, "-m", "src.bot.main"], ROOT)
    assert code == 0
