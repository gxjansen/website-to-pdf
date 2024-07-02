import asyncio
from pyppeteer import launch

async def generate_pdf(url, output_path):
    browser = await launch()
    page = await browser.newPage()
    try:
        await page.goto(url, {'waitUntil': 'networkidle0', 'timeout': 60000})

        # Remove unnecessary content and adjust layout
        await page.evaluate('''() => {
            function removeElements(selector) {
                document.querySelectorAll(selector).forEach(el => el.remove());
            }
            removeElements('header, footer, nav, .advertisement, .social-media-links');
            document.body.style.margin = '0';
            document.body.style.padding = '10px';
            const mainContent = document.querySelector('main') || document.querySelector('.main-content') || document.body;
            mainContent.style.width = '100%';
            mainContent.style.maxWidth = '800px';
            mainContent.style.margin = '0 auto';
        }''')

        # Set viewport for consistent rendering
        await page.setViewport({'width': 1024, 'height': 768})

        # Generate PDF with optimized settings
        await page.pdf({
            'path': output_path,
            'format': 'A4',
            'printBackground': True,
            'margin': {'top': '1cm', 'right': '1cm', 'bottom': '1cm', 'left': '1cm'},
            'preferCSSPageSize': True,
        })
        print(f"Generated PDF for {url}")
    except Exception as e:
        print(f"Error generating PDF for {url}: {e}")
    finally:
        await browser.close()