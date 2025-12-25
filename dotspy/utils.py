from typing import Optional
import subprocess
import tempfile
import os

def render_to_file(dot_source: str, output_path: str, format: str = "png"):
    """Render DOT source to file using graphviz."""
    # Write DOT source to a temp file
    # We use delete=False because we need to pass the filename to the subprocess
    with tempfile.NamedTemporaryFile(mode="w", suffix=".dot", delete=False) as f:
        f.write(dot_source)
        dot_file = f.name
    
    try:
        # Construct command: dot -Tformat input -o output
        cmd = ["dot", f"-T{format}", dot_file, "-o", output_path]
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        # Re-raise with stderr for better debugging
        raise RuntimeError(f"Graphviz failed: {e.stderr.decode('utf-8')}") from e
    except FileNotFoundError:
         raise RuntimeError("Graphviz 'dot' executable not found. Please install Graphviz.")
    finally:
        if os.path.exists(dot_file):
            os.unlink(dot_file)

def render_to_svg(dot_source: str) -> str:
    """Render DOT source to SVG string."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".dot", delete=False) as f:
        f.write(dot_source)
        dot_file = f.name
    
    try:
        result = subprocess.run(
            ["dot", "-Tsvg", dot_file],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Graphviz failed: {e.stderr}") from e
    except FileNotFoundError:
         raise RuntimeError("Graphviz 'dot' executable not found. Please install Graphviz.")
    finally:
        if os.path.exists(dot_file):
            os.unlink(dot_file)
