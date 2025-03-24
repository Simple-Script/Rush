import webview

def run_js_in_browser():
    # HTML content with embedded JS
    html_content = """
    <html>
    <body>
        <h1>Hello from Python</h1>
        <button onclick="alert('Hello from JavaScript!')">Click me</button>
        <script>
            document.body.innerHTML += "<p>Current time: " + new Date() + "</p>";
        </script>
    </body>
    </html>
    """

    # Launch the webview with the HTML content
    webview.create_window("JS with Python", html=html_content)
    webview.start()

if __name__ == "__main__":
    run_js_in_browser()
