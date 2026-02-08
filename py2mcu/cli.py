"""
Command-line interface for py2mcu
"""
import click
import sys
from pathlib import Path

@click.group()
@click.version_option()
def main():
    """py2mcu - Python to MCU C Compiler"""
    pass

@main.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--target', default='pc', help='Target platform (pc, stm32f4, esp32, rp2040)')
@click.option('--output', '-o', default='build', help='Output directory')
@click.option('--optimize', '-O', default='2', help='Optimization level (0-3)')
def compile(source, target, output, optimize):
    """Compile Python source to C code"""
    click.echo(f"Compiling {source} for {target}...")

    from py2mcu.compiler import Compiler

    compiler = Compiler(target=target, optimize=optimize)

    try:
        c_code = compiler.compile_file(source)

        output_path = Path(output)
        output_path.mkdir(exist_ok=True)

        output_file = output_path / Path(source).with_suffix('.c').name
        output_file.write_text(c_code)

        click.echo(f"✓ Generated: {output_file}")

    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)

@main.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--target', default='pc', help='Target platform')
def run(source, target):
    """Compile and run on PC (test mode)"""
    if target != 'pc':
        click.echo("Run command only supports PC target", err=True)
        sys.exit(1)

    click.echo(f"Running {source} on PC...")
    click.echo("(PC test mode - hardware calls are mocked)")

    # TODO: Implement PC execution

@main.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--target', required=True, help='Target MCU platform')
@click.option('--port', help='Serial port for flashing')
def deploy(source, target, port):
    """Compile and deploy to MCU"""
    click.echo(f"Deploying {source} to {target}...")

    # TODO: Implement deployment

if __name__ == '__main__':
    main()
