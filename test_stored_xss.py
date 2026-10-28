
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:5000"


def test_stored_comment_is_displayed_as_text():
    payload = "<img src=x onerror=alert('Stored XSS')>"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        alerts = []

        page.on("dialog", lambda dialog: alerts.append(dialog.message))

        response = page.request.post(
            f"{BASE_URL}/comments",
            form={"comment": payload},
        )
        assert response.status in (200, 302)

        page.goto(BASE_URL)

        comment = page.locator("li").filter(has_text=payload).last
        assert comment.count() == 1

        assert comment.count() >= 1
        assert comment.locator("img").count() == 0
        assert payload in comment.inner_text()
        assert alerts == []

        browser.close()


def test_normal_comment_is_displayed():
    comment_text = "Comentario de prueba automatizada"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        response = page.request.post(
            f"{BASE_URL}/comments",
            form={"comment": comment_text},
        )
        assert response.status in (200, 302)

        page.goto(BASE_URL)

        assert comment_text in page.locator("body").inner_text()

        browser.close()
