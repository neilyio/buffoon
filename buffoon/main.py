import subprocess
from pathlib import Path
from typing import Any

def format_heading(message: str) -> str:
    r = message.record
    t = r['time']
    date = f"{t.month}/{str(t.day).zfill(2)}"
    clock = f"{t.hour}:{str(t.minute).zfill(2)}"
    time = f"{date}/{clock}"
    return f"*** {time} {r['module']}::{r['line']}::{r['function']}"

def format_content(message: str) -> str:
    return message

def format_lisp(lisp: str, message: str, buffer_name:str = "*Buffoon Python Logs*") -> str:
    lisp = lisp.replace("{___PYTHON_PLACEHOLDER_BUFFER___}", buffer_name)
    lisp = lisp.replace("{___PYTHON_PLACEHOLDER_HEADING___}", format_heading(message))
    lisp = lisp.replace("{___PYTHON_PLACEHOLDER_CONTENT___}", format_content(message))
    return lisp

def read_template() -> str:
    template_path = Path(__file__).parent.parent.joinpath('template.el') 
    with open(template_path, "r") as f:
        return f.read()

def emacsclient(*args: str) -> None:
    result = subprocess.run(['emacsclient'] + list(args), stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise ChildProcessError(result.stderr.decode('windows-1252')) 

def buffoon(message: Any) -> None:
    lisp = format_lisp(read_template(), message)
    emacsclient('-e', '-u', lisp)
