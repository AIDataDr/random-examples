"""Launch Streamlit automatically, or use --existing to attach to a running server."""
import argparse
import subprocess
import sys
import time
import socket
import urllib.request
from pathlib import Path
import webview

ROOT = Path(__file__).resolve().parent
APP_TITLE = 'My Analytics Application'
APP_ICON = ROOT / 'assets/app.ico'
PORT = 8501
URL = f'http://127.0.0.1:{PORT}'

# EDIT THESE OPTIONS TO CUSTOMIZE YOUR DESKTOP WINDOW.
WINDOW_OPTIONS = dict(
    width=1200,          # Initial width in pixels
    height=800,          # Initial height in pixels
    min_size=(800, 600), # Minimum width and height
    x=None,              # None = default position; e.g. 100
    y=None,              # None = default position; e.g. 50
    resizable=True,      # Allow user to resize
    maximized=False,     # Start maximized (overrides initial size)
    minimized=False,     # Start minimized
    fullscreen=False,    # Start fullscreen (no normal title bar)
    frameless=False,     # Hide native title bar and borders
    confirm_close=True,  # Ask before closing
    on_top=False,        # Keep above other windows
    zoomable=True,       # Allow web content zooming
    background_color='#FFFFFF',
    text_select=True,    # Allow selecting text
)


def start_streamlit():
    # Avoid accidentally attaching to an unrelated server on this port.
    with socket.socket() as sock:
        try:
            sock.bind(('127.0.0.1', PORT))
        except OSError as exc:
            raise RuntimeError(f'Port {PORT} is busy. Use --existing or change PORT.') from exc
    return subprocess.Popen([
        sys.executable, '-m', 'streamlit', 'run', str(ROOT / 'app.py'),
        '--server.headless=true', '--server.address=127.0.0.1',
        f'--server.port={PORT}',
    ], cwd=ROOT)


def wait_for_streamlit(process=None, timeout=30):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process is not None and process.poll() is not None:
            raise RuntimeError('Streamlit exited before startup completed.')
        try:
            with urllib.request.urlopen(URL + '/_stcore/health', timeout=1) as response:
                if response.status == 200:
                    return
        except OSError:
            time.sleep(0.25)
    raise RuntimeError('Streamlit startup timed out. Check the server and port.')


def show_window():
    window = webview.create_window(title=APP_TITLE, url=URL, **WINDOW_OPTIONS)

    if sys.platform == 'win32':
        # Windows WinForms native icon; separate from Streamlit's favicon.
        # Closure accepts either zero arguments or an event-supplied window.
        def set_icon(*args):
            try:
                from System.Drawing import Icon
                window.native.Icon = Icon(str(APP_ICON))
                window.native.ShowIcon = True
            except Exception as exc:
                print(f'Could not set native window icon: {exc}', file=sys.stderr)
        window.events.before_show += set_icon
        webview.start(gui='edgechromium', debug=False)
    else:
        webview.start(debug=False, icon=str(ROOT / 'assets/logo.png'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--existing', action='store_true', help='Use an already running Streamlit server; leave it running on close.')
    args = parser.parse_args()
    server = None
    try:
        if not args.existing:
            server = start_streamlit()
        wait_for_streamlit(server)
        show_window()
    finally:
        if server is not None and server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()


if __name__ == '__main__':
    main()
