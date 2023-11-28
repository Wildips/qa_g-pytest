"""
Сделайте разные фикстуры для каждого теста, которые выставят размеры окна браузера
"""
import pytest
from selene.support.shared import browser
from selene import be, have


@pytest.fixture
def desktop_browser():
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.open("https://github.com").wait_until(
        have.title("GitHub: Let's build from here - GitHub")
    )
    yield browser
    browser.quit()


@pytest.fixture
def mobile_browser():
    browser.config.timeout = 2.0
    browser.config.window_width = 393
    browser.config.window_height = 852
    browser.open("https://github.com").wait_until(
        have.title("GitHub: Let's build from here - GitHub")
    )
    yield browser
    browser.quit()


def test_github_desktop(desktop_browser):
    # ARRANGE (GIVEN)

    # ACTIONS (WHEN)
    desktop_browser.element(".HeaderMenu-link--sign-in").should(be.clickable).click()

    # ASSERT (THEN)
    desktop_browser.element(".auth-form-header").should(have.text("Sign in to GitHub"))


def test_github_mobile(mobile_browser):
    # ARRANGE (GIVEN)

    # ACTIONS (WHEN)
    mobile_browser.element(".Button-label").should(be.clickable).click()
    mobile_browser.element(".d-inline-block.d-lg-none").should(be.clickable).click()
    mobile_browser.element(".HeaderMenu-link--sign-in").with_(
        timeout=browser.config.timeout * 4
    ).should(be.visible).click()

    # ASSERT (THEN)
    mobile_browser.element(".auth-form-header").should(have.text("Sign in to GitHub"))
