from django.template.loaders.filesystem import Loader as FileSystemLoader
from django.template.loaders.app_directories import Loader as AppDirectoriesLoader
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)

IDE_TO_URI_MAPPER = {
    "atom": "atom://core/open/file?filename=",
    "codelite": "codelite://open?file=",
    "cursor": "cursor://file/",
    "emacs": "emacs://open?url=",
    "espresso": "x-espresso://open?filepath=",
    "idea": "idea://open?file=",
    "macvim": "mvim://open/?url=",
    "netbeans": "netbeans://open/?f=",
    "nova": "nova://open?path=",
    "pycharm": "pycharm://open?file=",
    "sublime": "subl://open?url=",
    "textmate": "txmt://open?url=",
    "vscode": "vscode://file/",
    "vscode-insiders": "vscode-insiders://file/",
    "vscode-insiders-remote": "vscode-insiders://vscode-remote/",
    "vscode-remote": "vscode://vscode-remote/",
    "vscodium": "vscodium://file/",
    "xdebug": "xdebug://",
}


def _get_setting_or_env(name):
    # Prefer Django setting, fall back to environment variable
    return getattr(settings, name, None) or os.environ.get(name)


def _inject_ide_link(source_content, template_name, filename):
    touchable_templates_ide = _get_setting_or_env("TOUCHABLE_TEMPLATES_IDE")
    custom_uri = IDE_TO_URI_MAPPER.get(touchable_templates_ide)
    touchable_templates_root = _get_setting_or_env("TOUCHABLE_TEMPLATES_ROOT") or ""
    touchable_templates_remove_prefix = _get_setting_or_env("TOUCHABLE_TEMPLATES_REMOVE_PREFIX") or ""

    try:
        # compute a relative path portion if a remove-prefix was provided
        rel_path = filename
        if touchable_templates_remove_prefix and filename.startswith(touchable_templates_remove_prefix):
            rel_path = filename[len(touchable_templates_remove_prefix):]

        absolute_template_path = (custom_uri or "") + touchable_templates_root + rel_path
    except Exception:
        absolute_template_path = filename

    # If template extends another template, we avoid wrapping the child; Django
    # templates are compiled in processor order so this is a best-effort approach.

    bordered = (
        f'<div class="touchable-templates-container" '
        f'data-template-name="{template_name}" '
        f'data-template-path="{absolute_template_path}" '
        f'style="display: block;">{source_content}</div>'
    )

    return bordered


class TouchableTemplatesLoader(FileSystemLoader):
    """A drop-in replacement for Django's filesystem.Loader that wraps
    template source in a touchable-templates container when enabled.

    To use: in `TEMPLATES[...]['OPTIONS']['loaders']` reference
    `touchable_templates.django.loader.TouchableTemplatesLoader` instead of
    `django.template.loaders.filesystem.Loader`.
    """

    def get_contents(self, origin):
        source = super().get_contents(origin)

        enabled = _get_setting_or_env("TOUCHABLE_TEMPLATES_ENABLE")
        if not enabled:
            return source

        try:
            template_name = getattr(origin, "template_name", None) or getattr(origin, "name", "")
            filename = getattr(origin, "name", "")
            return _inject_ide_link(source, template_name, filename)
        except Exception:
            logger.exception("touchable_templates: failed to inject IDE link into Django template")
            return source


class TouchableTemplatesAppDirectoriesLoader(AppDirectoriesLoader):
    """A drop-in replacement for Django's app_directories.Loader that wraps
    template source in a touchable-templates container when enabled.

    To use: in `TEMPLATES[...]['OPTIONS']['loaders']` reference
    `touchable_templates.django.loader.TouchableTemplatesAppDirectoriesLoader` instead of
    `django.template.loaders.app_directories.Loader`.
    """

    def get_contents(self, origin):
        source = super().get_contents(origin)

        enabled = _get_setting_or_env("TOUCHABLE_TEMPLATES_ENABLE")
        if not enabled:
            return source

        try:
            template_name = getattr(origin, "template_name", None) or getattr(origin, "name", "")
            filename = getattr(origin, "name", "")
            return _inject_ide_link(source, template_name, filename)
        except Exception:
            logger.exception("touchable_templates: failed to inject IDE link into Django app template")
            return source
