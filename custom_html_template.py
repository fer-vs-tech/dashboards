# Override the default HTML template for the dashboard with custom favicon
WM_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        <link rel="shortcut icon" href="/dash/static/assets/favicon.ico">
        {%css%}
    </head>
    <body>
        <script src="/dash/static/library/jquery-3.5.1.js"></script>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
