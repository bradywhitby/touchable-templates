let altToggled = false;

// Append the element to the DOM, for example, to the body
var elemDiv = document.createElement('div');
elemDiv.id = 'floating-template-name';
elemDiv.style.cssText = "display: none; position: absolute; background: white; border: 1px solid black; padding: 5px; z-index: 9999;"
document.body.appendChild(elemDiv);
const floatingElement = document.getElementById("floating-template-name");    

document.addEventListener("DOMContentLoaded", function(event) {

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Alt') {
            altToggled = !altToggled;
            if (!altToggled) {
                floatingElement.style.display = 'none';
            }
        }
    });

    document.addEventListener('click', function(event) {
        if (altToggled) {
            let closestElement = event.target.closest('.touchable-templates');
            if (closestElement) {
                let templatePath = closestElement.getAttribute('data-template-path');
                if (templatePath) {
                    window.open(templatePath, '_blank');
                    event.stopPropagation();
                }
            }
        }
    }, true);

    document.addEventListener('mousemove', (e) => {
        if (!altToggled) return;
        const el = e.target.closest('.touchable-templates');
        if (!el) return floatingElement.style.display = 'none';

        const name = el.getAttribute('data-template-name');
        if (!name) return;

        floatingElement.textContent = name;
        floatingElement.style.display = 'block';
        const { pageX: x, pageY: y } = e;
        const { offsetWidth: w, offsetHeight: h } = floatingElement;
        const { innerWidth: vw, innerHeight: vh } = window;
        floatingElement.style.left = `${x + w + 20 > vw ? x - w - 5 : x + 10}px`;
        floatingElement.style.top = `${y + h + 20 > vh ? y - h - 5 : y + 10}px`;
    });

    document.addEventListener('mouseleave', () => {
        floatingElement.style.display = 'none';
    });

    document.addEventListener('mouseenter', (e) => {
        if (altToggled) {
            const el = e.target.closest('.touchable-templates');
            if (el) {
                const name = el.getAttribute('data-template-name');
                floatingElement.textContent = name;
                floatingElement.style.display = 'block';
            }
        }
    });

});
