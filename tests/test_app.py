import os
import time
import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.app import get_unique_filename, convert_file, convert

@pytest.fixture(scope="module")
def setup_teardown():
    input_folder = 'test_input'
    output_folder = 'test_output'
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    yield input_folder, output_folder

    for folder in [input_folder, output_folder]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            os.remove(file_path)
        os.rmdir(folder)

def create_test_file(folder, filename, content=b''):
    with open(os.path.join(folder, filename), 'wb') as f:
        f.write(content)

def test_get_unique_filename_FileDoesNotExist_ReturnsOriginalFilename(setup_teardown):
    input_folder, output_folder = setup_teardown
    output_path = os.path.join(output_folder, 'test.txt')
    unique_filename = get_unique_filename(output_path)
    assert unique_filename == output_path

def test_get_unique_filename_FileExists_ReturnsUniqueFilename(setup_teardown):
    input_folder, output_folder = setup_teardown
    output_path = os.path.join(output_folder, 'test.txt')
    with open(output_path, 'w') as f:
        f.write('existing content')
    unique_filename = get_unique_filename(output_path)
    assert unique_filename != output_path
    assert unique_filename.startswith(output_path)

@patch('subprocess.Popen')
def test_convert_file_NonVideoFile_ConvertsSuccessfully(mock_popen, setup_teardown):
    input_folder, output_folder = setup_teardown
    input_file = os.path.join(input_folder, 'test.png')
    create_test_file(input_folder, 'test.png', b'PNG content')
    convert_file(input_file, output_folder, 'jpg')
    output_file = os.path.join(output_folder, 'test.jpg')
    assert os.path.exists(output_file)

@patch('subprocess.Popen')
def test_convert_file_VideoFile_ConvertsSuccessfully(mock_popen, setup_teardown):
    input_folder, output_folder = setup_teardown
    input_file = os.path.join(input_folder, 'test.mp4')
    create_test_file(input_folder, 'test.mp4', b'MP4 content')
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_popen.return_value = mock_process
    convert_file(input_file, output_folder, 'avi')
    output_file = os.path.join(output_folder, 'test.avi')
    assert os.path.exists(output_file)

@patch('subprocess.Popen')
def test_convert_file_ConversionFails_HandlesGracefully(mock_popen, setup_teardown):
    input_folder, output_folder = setup_teardown
    input_file = os.path.join(input_folder, 'test.mp4')
    create_test_file(input_folder, 'test.mp4', b'MP4 content')
    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_process.stderr.read.return_value = b'Conversion failed'
    mock_popen.return_value = mock_process
    convert_file(input_file, output_folder, 'avi')
    output_file = os.path.join(output_folder, 'test.avi')
    assert not os.path.exists(output_file)

@patch('concurrent.futures.ThreadPoolExecutor')
def test_convert_MultipleFiles_ConvertsSuccessfully(mock_executor, setup_teardown):
    input_folder, output_folder = setup_teardown
    input_files = [
        os.path.join(input_folder, 'test1.png'),
        os.path.join(input_folder, 'test2.mp4')
    ]
    for file in input_files:
        create_test_file(input_folder, os.path.basename(file), b'content')
    mock_executor.return_value.submit = MagicMock()
    convert(input_files, output_folder, 'jpg')
    assert mock_executor.return_value.submit.called

@patch('concurrent.futures.ThreadPoolExecutor')
def test_convert_EmptyInputList_NoConversion(mock_executor, setup_teardown):
    input_folder, output_folder = setup_teardown
    convert([], output_folder, 'jpg')
    assert not mock_executor.return_value.submit.called
