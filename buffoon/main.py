import subprocess
from pathlib import Path
from typing import Optional, Callable, Any


def default_heading() -> str:
    return "* HeadingTest"


def loguru_heading(message: Any) -> str:
    r = message.record
    t = r['time']
    date = f"{t.month}/{str(t.day).zfill(2)}"
    clock = f"{t.hour}:{str(t.minute).zfill(2)}"
    time = f"{date}/{clock}"
    return f"* {time} {r['module']}::{r['line']}::{r['function']}"


def loguru_content(message: Any) -> str:
    return message.record['message']


def which(program: str) -> Optional[str]:
    """
    Replicates the functionality of the UNIX which command.
    Returns the path of the excetuable if it exists on the PATH.
    If not found, returns None.
    """
    import os

    def is_exe(fpath):
        pathexts = os.environ["PATHEXT"].split(os.pathsep)
        pathexts.append("")
        for p in pathexts:
            for ext in [p.lower(), p.upper()]:
                spath = fpath + ext
                if os.path.isfile(spath) and os.access(spath, os.X_OK):
                    return True
        return False

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def format_lisp(buffer_name, heading: str, content: str, lisp: str) -> str:
    lisp = lisp.replace("{___PYTHON_PLACEHOLDER_BUFFER___}", buffer_name)
    lisp = lisp.replace("{___PYTHON_PLACEHOLDER_HEADING___}", heading)
    lisp = lisp.replace("{___PYTHON_PLACEHOLDER_CONTENT___}", content)
    return lisp


def read_template() -> str:
    template_path = Path(__file__).parent.parent.joinpath('template.el')
    with open(template_path, "r") as f:
        return f.read()


def emacsclient(*args: str) -> None:
    if not which('emacsclient'):
        raise FileNotFoundError("Could not find 'emacsclient' on the $PATH.")
    result = subprocess.run(['emacsclient'] + list(args),
                            stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise ChildProcessError(result.stderr.decode('windows-1252'))


def buffoon(message: Any,
            buffer_name: str = "*Buffoon Python Logs*",
            heading_parser: Optional[Callable[[str], str]] = None,
            content_parser: Optional[Callable[[str], str]] = None) -> None:
    heading = heading_parser(message) if heading_parser else default_heading()
    content = content_parser(message) if content_parser else ""
    lisp = format_lisp(buffer_name, heading, content, read_template())
    emacsclient('-e', '-u', lisp)


def loguru_buffoon(message: Any) -> None:
    buffoon(message,
            heading_parser=loguru_heading,
            content_parser=loguru_content)
