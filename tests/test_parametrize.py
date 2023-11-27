"""
Переопределите параметр с помощью indirect параметризации на уровне теста
"""
import pytest
from selene.support.shared import browser
from selene import be, have


@pytest.fixture(params=["desktop", "mobile"], scope="function")
def browser_size(request):
    browser.config.timeout = 2.0
    if request.param == "desktop":
        browser.config.window_width = 1920
        browser.config.window_height = 1080
    if request.param == "mobile":
        browser.config.window_width = 393
        browser.config.window_height = 852
    browser.open("https://github.com").wait_until(
        have.title("GitHub: Let's build from here - GitHub")
    )
    yield browser
    browser.quit()


@pytest.mark.parametrize("browser_size", ["desktop"], indirect=True)
def test_github_desktop_params(browser_size):
    # ARRANGE (GIVEN)
    # browser_size.open("https://github.com").wait_until(
    #     have.title("GitHub: Let's build from here - GitHub")
    # )

    # ACTIONS (WHEN)
    browser_size.element(".HeaderMenu-link--sign-in").should(be.clickable).click()

    # ASSERT (THEN)
    browser_size.element(".auth-form-header").should(have.text("Sign in to GitHub"))


@pytest.mark.parametrize("browser_size", ["mobile"], indirect=True)
def test_github_mobile_params(browser_size):
    # ARRANGE (GIVEN)
    # browser.open("https://github.com").wait_until(
    #     have.title("GitHub: Let's build from here - GitHub")
    # )

    # ACTIONS (WHEN)
    browser_size.element(".Button-label").should(be.clickable).click()
    browser_size.element(".d-inline-block.d-lg-none").should(be.clickable).click()
    browser_size.element(".HeaderMenu-link--sign-in").with_(
        timeout=browser.config.timeout * 4
    ).should(be.visible).click()

    # ASSERT (THEN)
    browser_size.element(".auth-form-header").should(have.text("Sign in to GitHub"))
