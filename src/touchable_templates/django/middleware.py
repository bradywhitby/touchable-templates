from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from bs4 import BeautifulSoup


class TouchableTemplatesMiddleware(MiddlewareMixin):
    """
    Middleware to post-process Django template responses and mark children with
    the `touchable-templates` class so the client script can provide IDE links.
    """

    def process_response(self, request, response):
        if not getattr(settings, "TOUCHABLE_TEMPLATES_ENABLE", False):
            return response

        content_type = response.get('Content-Type', '').split(';')[0]
        if content_type != 'text/html':
            return response
        
        # Decode the response content
        content = response.content.decode(response.charset)
        soup = BeautifulSoup(content, 'html.parser')

        # Find all elements with class 'touchable-templates-container'
        containers = soup.find_all(class_='touchable-templates-container')
        for container in containers:
            # Get data attributes from the container
            data_template_name = container.get('data-template-name')
            data_template_path = container.get('data-template-path')

            # Iterate over direct children of the container
            for child in container.find_all(recursive=False):
                # Add 'touchable-templates' class to the child
                existing_classes = child.get('class', [])
                if 'touchable-templates' not in existing_classes:
                    child['class'] = existing_classes + ['touchable-templates']

                # Copy data attributes to the child
                if data_template_name:
                    child['data-template-name'] = data_template_name
                if data_template_path:
                    child['data-template-path'] = data_template_path

            # Remove the container but keep its children
            container.unwrap()

        # Update the response content
        updated_content = str(soup).encode(response.charset)
        response.content = updated_content
        response['Content-Length'] = len(response.content)

        return response
