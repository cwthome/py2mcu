import os
import subprocess
import sys
import tempfile
import pytest


DEMOS = [
    'demo1_led_blink',
    'demo2_adc_average',
    'demo3_inline_c',
    'demo4_memory',
    'demo5_docstring_c',
    'demo6_defines',
]

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'examples')
RUNTIME_DIR = os.path.join(os.path.dirname(__file__), '..', 'runtime')


class TestDemosCompilation:
    @pytest.mark.parametrize('demo', DEMOS)
    def test_compile_demo(self, demo):
        source_file = os.path.join(EXAMPLES_DIR, f'{demo}.py')
        assert os.path.exists(source_file), f'Source file not found: {source_file}'

        result = subprocess.run(
            [sys.executable, '-m', 'py2mcu.cli', 'compile',
             source_file, '--target', 'pc', '-o', '/tmp/py2mcu_test/'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f'Compilation failed: {result.stderr}'
        assert os.path.exists(f'/tmp/py2mcu_test/{demo}.c'), 'C file not generated'


class TestDemosBuild:
    @pytest.mark.parametrize('demo', DEMOS)
    def test_build_demo(self, demo):
        c_file = f'/tmp/py2mcu_test/{demo}.c'
        if not os.path.exists(c_file):
            pytest.skip(f'C file not found: {c_file}')

        result = subprocess.run(
            ['gcc', '-I', RUNTIME_DIR, c_file,
             os.path.join(RUNTIME_DIR, 'gc_runtime.c'),
             '-o', f'/tmp/py2mcu_test/{demo}'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f'Build failed: {result.stderr}'
        assert os.path.exists(f'/tmp/py2mcu_test/{demo}'), 'Executable not created'


class TestDemoExecution:
    def test_demo4_memory_execution(self):
        exe = '/tmp/py2mcu_test/demo4_memory'
        if not os.path.exists(exe):
            pytest.skip('Executable not found')

        result = subprocess.run(
            [exe],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, f'Execution failed: {result.stderr}'
        assert 'Memory Management Demo' in result.stdout
        assert 'Stack allocation' in result.stdout

    def test_demo5_execution(self):
        exe = '/tmp/py2mcu_test/demo5_docstring_c'
        if not os.path.exists(exe):
            pytest.skip('Executable not found')

        result = subprocess.run(
            [exe],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, f'Execution failed: {result.stderr}'
        assert 'Demo 5' in result.stdout


class TestTargetPlatforms:
    @pytest.mark.parametrize('target', ['pc', 'stm32f4', 'esp32', 'rp2040'])
    def test_compile_all_targets(self, target):
        source_file = os.path.join(EXAMPLES_DIR, 'demo1_led_blink.py')
        result = subprocess.run(
            [sys.executable, '-m', 'py2mcu.cli', 'compile',
             source_file, '--target', target, '-o', '/tmp/py2mcu_test/'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f'Failed for target {target}: {result.stderr}'
        c_file = '/tmp/py2mcu_test/demo1_led_blink.c'
        assert os.path.exists(c_file)
        with open(c_file) as f:
            content = f.read()
        expected_macro = f'TARGET_{target.upper()}'
        assert f'#define {expected_macro} 1' in content


class TestEdgeCases:
    def test_empty_function(self):
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('def foo() -> None:\n    pass\n')
            f.flush()
            temp_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, '-m', 'py2mcu.cli', 'compile',
                 temp_path, '--target', 'pc', '-o', '/tmp/py2mcu_test/'],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
        finally:
            os.unlink(temp_path)

    def test_nested_loops(self):
        import tempfile
        code = '''
def foo() -> None:
    i: int = 0
    while i < 5:
        j: int = 0
        while j < 5:
            j = j + 1
        i = i + 1
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.flush()
            temp_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, '-m', 'py2mcu.cli', 'compile',
                 temp_path, '--target', 'pc', '-o', '/tmp/py2mcu_test/'],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
        finally:
            os.unlink(temp_path)

    def test_multiple_c_code_blocks(self):
        import tempfile
        code = '''
def foo() -> None:
    """__C_CODE__
    int x = 1;
    """
    pass

def bar() -> None:
    """__C_CODE__
    int y = 2;
    """
    pass
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.flush()
            temp_path = f.name

        try:
            result = subprocess.run(
                [sys.executable, '-m', 'py2mcu.cli', 'compile',
                 temp_path, '--target', 'pc', '-o', '/tmp/py2mcu_test/'],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
        finally:
            os.unlink(temp_path)


def setup_module(module):
    os.makedirs('/tmp/py2mcu_test', exist_ok=True)
