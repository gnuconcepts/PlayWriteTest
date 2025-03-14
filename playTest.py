import json
from playwright.sync_api import sync_playwright

def extract_dom_with_coordinates():
    with sync_playwright() as p:
        
        # Prompt for domain input
        domain = input("Enter the domain (e.g., example.com): ").strip()
        if not domain.startswith("http"):
            domain = "https://" + domain
        browser = p.chromium.launch(headless=False)  # Open browser in visible mode
        page = browser.new_page()

        page.goto(domain)

        # Load and execute the JavaScript file
        with open("buildDomTree.js", "r", encoding="utf-8") as f:
            dom_script = f.read()

        dom_tree = page.evaluate(dom_script, {
            "doHighlightElements": True,
            "focusHighlightIndex": -1,
            "viewportExpansion": 0
        })

        # Save results to a JSON file
        with open("dom_tree_with_coordinates.json", "w", encoding="utf-8") as f:
            json.dump(dom_tree, f, indent=4)

        print("DOM tree with coordinates saved to dom_tree_with_coordinates.json")

        # Click on the textbox and enter text using the 'name' attribute
        try:
            text_box = page.locator("textarea[name='q']")  # Using 'name' selector
            text_box.click()
            text_box.fill("Playwright test search")  # Enter text
            print("Successfully entered text in the search box.")
        except Exception as e:
            print(f"Failed to interact with textbox: {e}")

        page.wait_for_timeout(30000)  # Wait for 30 seconds before closing
        browser.close()

extract_dom_with_coordinates()
