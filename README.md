
# touchable-templates

touchable-templates is a small developer helper that wraps rendered templates in a lightweight
HTML marker and ships a tiny client-side script so you can, for example, click
on a rendered component in the browser to automatically open the source template in your IDE.

This package is purposely minimal and designed to be installed into Django projects.
Note: Future versions may support Jinja2, Flask, and other frameworks. This package is not intended to be used in production.

## Key features

- Server-side wrapper for Django template responses (middleware)
- Small client-side script included as package static files

## Installation

### pip install

```bash
pip install touchable-templates
```

### uv install

```bash
uv add touchable-templates
```

## Django integration (quick start)

1. Add the app to your `INSTALLED_APPS` in `settings.py`:

```py
INSTALLED_APPS = [
    # ...
  "touchable_templates",
]
```

2. Add the middleware so HTML responses are post-processed to convert wrapper containers
  into elements with the `touchable-templates` class (the client script uses that):

```py
MIDDLEWARE = [
    # ...
  "touchable_templates.django.middleware.TouchableTemplatesMiddleware",
    # ...
]
```

3. Configure enablement and IDE mapping. You can set these via environment variables or
   in `settings.py`. Example (development):

```py
# TOUCHABLE_TEMPLATES settings (example)
TOUCHABLE_TEMPLATES_ENABLE = True
TOUCHABLE_TEMPLATES_IDE = "vscode"
# Optional settings: Use if your project is dockerized or paths need adjustment
TOUCHABLE_TEMPLATES_ROOT = "/full/path/to/your/project/root/on/local/machine"
TOUCHABLE_TEMPLATES_REMOVE_PREFIX = "project/root/in/docker/container"
```

## Supported IDEs

- `atom`
- `codelite`
- `cursor`
- `emacs`
- `espresso`
- `idea`
- `macvim`
- `netbeans`
- `nova`
- `pycharm`
- `sublime`
- `textmate`
- `vscode`
- `vscode-insiders`
- `vscode-insiders-remote`
- `vscode-remote`
- `vscodium`
- `xdebug`

4. Include the client JavaScript in your base template (requires `django.contrib.staticfiles`):
Add Script tag at the end of the body, or in the head.

```django
{% load static %}
<script src="{% static 'js/touchable_templates.js' %}"></script>
```

## Use

Press the `alt` or `opt` key to toggle the functionality on and off.
Moving your mouse around the page you will see a floating element indicating the template path/name
Click on any element on the page to open the corresponding template in your configured IDE.

## Notes

- The middleware only processes responses with `Content-Type: text/html` to ensure we are not processing json requests.
- Make sure `TOUCHABLE_TEMPLATES_ENABLE` is `True` in development and `False` in production.
- Use `TOUCHABLE_TEMPLATES_REMOVE_PREFIX` to strip any leading path segments that are
  not part of the local filesystem path (e.g. if your project runs in a Docker container
  with a different root path).

## Troubleshooting

- No overlay appears: verify `TOUCHABLE_TEMPLATES_ENABLE` is True and the JS is loaded correctly (check browser devtools network tab).
- Alt-click does nothing: ensure the HTML elements have `touchable-templates` class (middleware unwraps container into children).

## License

MIT License (MIT)
