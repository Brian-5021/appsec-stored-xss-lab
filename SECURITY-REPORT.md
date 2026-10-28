
# Stored XSS Lab — Security Report

## 1. Summary

This lab demonstrates a stored user-comment workflow using Flask, SQLite, Jinja2, and Playwright. The original template rendered user-controlled comments without HTML escaping by applying Jinja's `safe` filter.

The filter was removed to restore automatic HTML escaping. Two automated tests passed after the change.

## 2. Affected component

- Application: Flask comment application
- Storage: SQLite
- Rendering: Jinja2 HTML template
- Vulnerable template expression: `{{ comment | safe }}`
- Corrected expression: `{{ comment }}`

## 3. Root cause

The `safe` filter marks the comment as safe for HTML rendering and disables Jinja's automatic escaping for that value.

Because the comment is stored and later rendered, unsafe HTML content can persist and be interpreted by the browser when the comment page is viewed.

## 4. Test evidence

The following behavior was observed:

- A normal comment remained visible after reloading the page.
- The test comment containing an `<img>` element was stored and retrieved.
- In the vulnerable version, browser DevTools showed an actual `<img>` element with an `onerror` attribute.
- JavaScript execution was not conclusively confirmed during the manual demonstration.

## 5. Remediation

Removed the `safe` filter from the comment output:

```html
<li>{{ comment }}</li>
```

Jinja's automatic HTML escaping then causes the comment to be displayed as text rather than interpreted as HTML markup.

## 6. Regression tests

Automated tests were run with pytest and Playwright:

- `test_stored_comment_is_displayed_as_text` — PASSED
- `test_normal_comment_is_displayed` — PASSED

Result: 2 passed.

The tests verify that the test comment is rendered as text, that an `<img>` element is not created from the comment, that no alert dialog is observed, and that normal comments remain visible.

## 7. Limitations

This is a local educational lab, not a complete security assessment. The manual test did not conclusively demonstrate JavaScript execution before remediation. Passing regression tests validate only the tested scenarios and do not prove that the entire application is free from XSS.

## 8. Lessons learned

- Trace untrusted data from its source through storage to its output sink.
- Stored content is not automatically safe because it is saved in a database.
- Avoid disabling template autoescaping for untrusted comments.
- Validate remediations with regression tests.
