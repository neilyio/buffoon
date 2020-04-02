import pytest
from pathlib import Path
from mock_lisp import MockLispTemplate, MockLispFormatted
import buffoon.main as m

MockBufferName = "Some day, when I'm awfully low"
MockHeading = "When the world is cold"
MockContents = "I will feel a glow just thinking of you\nAnd the way you look tonight"
Buffer = "{___PYTHON_PLACEHOLDER_BUFFER___}"
Heading = "{___PYTHON_PLACEHOLDER_HEADING___}"
Content = "{___PYTHON_PLACEHOLDER_CONTENT___}"

@pytest.fixture
def mock_run(mocker):
    error_string = "*ERROR* Lisp process did not finish correctly."
    mock_run = mocker.patch('subprocess.run', autospec=True)
    mock_run.return_value.returncode = 0
    mock_run.return_value.stderr = error_string.encode('windows-1252') 
    return mock_run

def test_read_template(mocker):
    # It returns the string contents of the template file.
    mock_open = mocker.mock_open(read_data=MockContents)
    mocker.patch('buffoon.main.open', mock_open)
    assert m.read_template() == MockContents
    # It opens a template file that exists.
    args = mock_open.call_args
    assert Path(args[0][0]).exists()

def test_format_lisp(mocker):
    mock_fmt_heading = mocker.MagicMock(return_value=MockHeading)
    mock_fmt_content = mocker.MagicMock(return_value=MockContents)
    mocker.patch.object(m, 'format_heading', mock_fmt_heading)
    mocker.patch.object(m, 'format_content', mock_fmt_content)
    # It replaces the buffer placeholder.
    # It replaces the content placeholder.
    # It replaces the heading placeholder.
    assert m.format_lisp(MockLispTemplate, None, buffer_name=MockBufferName) == MockLispFormatted

def test_format_content():
    # It returns content unchanged.
    assert m.format_content(MockContents) == MockContents

def test_buffoon(mocker):
    # It calls emacs client with formatted lisp.
    mocker.patch.object(m, "format_lisp", mocker.MagicMock(return_value=MockLispFormatted))
    mock_ec = mocker.patch.object(m, 'emacsclient', mocker.MagicMock())
    m.buffoon(MockContents)
    mock_ec.assert_called_once_with('-e', '-u', MockLispFormatted)

def test_emacsclient(mocker, mock_run):
    m.emacsclient('-e', '-u', MockLispTemplate)
    # It calls subprocess.run with valid arguments.
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args[0] == 'emacsclient'
    assert all(arg.startswith('-') for arg in args [1:-1])
    assert args[-1] == MockLispTemplate
    # It raises an error without a valid return code.
    mock_run.return_value.returncode = 1
    with pytest.raises(ChildProcessError) as err:
        m.emacsclient('-e', '-u', MockLispTemplate)
    # The error contains the output from subprocess.run.
    assert mock_run.return_value.stderr.decode('windows-1252') in str(err.value)
