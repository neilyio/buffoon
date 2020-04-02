import pytest
from pathlib import Path
import buffoon.main as m

MockBufferName = "MyMockName"
MockHeading = "MyMockHeading"
MockContents = "MyMockContents"
Buffer = "{___PYTHON_PLACEHOLDER_BUFFER___}"
Heading = "{___PYTHON_PLACEHOLDER_HEADING___}"
Content = "{___PYTHON_PLACEHOLDER_CONTENT___}"
MockTemplate = f"___PY___{Buffer}___PL___{Heading}___{Content}"
MockFormattedTemplate = f"___PY___{MockBufferName}___PL___{MockHeading}___{MockContents}"

@pytest.fixture
def mock_run(mocker):
    return mocker.patch('subprocess.run', autospec=True)

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
    assert m.format_lisp(MockTemplate, None, buffer_name=MockBufferName) == MockFormattedTemplate

def test_format_content():
    # It returns content unchanged.
    assert m.format_content(MockContents) == MockContents

def test_buffoon(mocker, mock_run):
    # It calls emacs client with formatted lisp.
    mock_format_lisp = mocker.Mock(return_value=MockFormattedTemplate)
    mocker.patch.object(m, 'format_lisp', mock_format_lisp)
    m.buffoon(MockContents)
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert 'emacsclient' in args
    assert MockFormattedTemplate in args
