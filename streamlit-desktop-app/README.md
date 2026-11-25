# Streamlit Desktop App

Windows example using Python, Streamlit, Plotly and pywebview (Edge WebView2).
Install the Microsoft Edge WebView2 Runtime if it is missing.

## Quick start
Open the extracted folder in VS Code and use your chosen Python environment.

```powershell
python -m pip install -r requirements.txt
python desktop.py
```

The launcher starts Streamlit and stops its own server when the window closes.

## Already running Streamlit?
In one terminal run `python -m streamlit run app.py` and in another run
`python desktop.py --existing`. Closing the window leaves that server running.
Change PORT in desktop.py to match your existing server if needed. The launcher
uses loopback only; it does not expose your app to other computers.

## Customize
Edit WINDOW_OPTIONS at the top of desktop.py for initial width, height, minimum
size, position, resize, maximize, minimize, fullscreen, frameless, close
confirmation, always-on-top, zoom, text selection and background color.
For a normal sized window, keep maximized, minimized and fullscreen False.
Avoid combining conflicting window modes. Frameless hides the native title bar.
Edit APP_TITLE for the native title and APP_ICON for the native Windows icon.
Edit st.set_page_config in app.py for the browser page title and favicon.
The favicon is not visible in pywebview because there are no browser tabs.
The Windows taskbar icon may differ when launched via python.exe.
Replace assets/logo.png and assets/app.ico with your own files, or regenerate
both with `python create_icon.py`. The included icons are ready to use.
Edit .streamlit/config.toml for theme and Streamlit server options. Restart after
changing server settings. For development, change fileWatcherType to "auto".

## Compatibility
Designed for Windows and pywebview 5.3+. Native icon behavior depends on the
backend/version; the launcher reports an icon failure without closing the app.
Python syntax and icon files were checked; the Windows GUI was not run here.
The example is source code, not a packaged Windows executable.
