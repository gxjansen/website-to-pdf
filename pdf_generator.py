import asyncio
from pyppeteer import launch

async def generate_pdf(url, output_path):
    browser = await launch()
    page = await browser.newPage()
    try:
        await page.goto(url, {'waitUntil': 'networkidle0', 'timeout': 60000})

        # Remove generic content
        await page.evaluate('''() => {
            // Function to remove elements by selector
            function removeElements(selector) {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => el.remove());
            }

            // Remove header
            removeElements('header');

            // Remove footer
            removeElements('footer');

            // Remove navigation menus (adjust selectors as needed)
            removeElements('nav');
            removeElements('.menu');
            removeElements('#sidebar');

            // Remove any other generic elements
            removeElements('.advertisement');
            removeElements('.social-media-links');

            // Adjust the main content to full width if needed
            const mainContent = document.querySelector('main') || document.querySelector('.main-content');
            if (mainContent) {
                mainContent.style.width = '100%';
                mainContent.style.margin = '0';
                mainContent.style.padding = '20px';
            }
        }''')

        # Generate PDF
        await page.pdf({'path': output_path, 'format': 'A4'})
        print(f"Generated PDF for {url}")
    except Exception as e:
        print(f"Error generating PDF for {url}: {e}")
    finally:
        await browser.close()
