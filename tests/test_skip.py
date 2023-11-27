"""
Параметризуйте фикстуру несколькими вариантами размеров окна
Пропустите мобильный тест, если соотношение сторон десктопное (и наоборот)
"""
import pytest
from selene.support.shared import browser
from selene import be, have

DEVICES_DICT = {
    "mobile": (393, 852),
    "desktop": (1080, 1920),
}


@pytest.fixture(
    params=[DEVICES_DICT["desktop"], DEVICES_DICT["mobile"]], scope="function"
)
def browser_config(request):
    browser.config.timeout = 2.0
    browser.config.window_width = request.param[0]
    browser.config.window_height = request.param[1]
    # browser.open("https://github.com").wait_until(
    #     have.title("GitHub: Let's build from here - GitHub")
    # )
    yield browser, [
        key
        for key, value in DEVICES_DICT.items()
        if value == (request.param[0], request.param[1])
    ][0]
    browser.quit()


def test_github_desktop_skip(browser_config):
    # ARRANGE (GIVEN)
    test_browser, browser_type = browser_config
    if browser_type == "mobile":
        pytest.skip(reason="Test can be executed under PC UI only")

    test_browser.open("https://github.com").wait_until(
        have.title("GitHub: Let's build from here - GitHub")
    )

    # ACTIONS (WHEN)
    test_browser.element(".HeaderMenu-link--sign-in").should(be.clickable).click()

    # ASSERT (THEN)
    test_browser.element(".auth-form-header").should(have.text("Sign in to GitHub"))


def test_github_mobile_skip(browser_config):
    # ARRANGE (GIVEN)
    test_browser, browser_type = browser_config
    if browser_type == "desktop":
        pytest.skip(reason="Test can be executed under mobile UI only")

    test_browser.open("https://github.com").wait_until(
        have.title("GitHub: Let's build from here - GitHub")
    )

    # ACTIONS (WHEN)
    test_browser.element(".Button-label").should(be.clickable).click()
    test_browser.element(".d-inline-block.d-lg-none").should(be.clickable).click()
    test_browser.element(".HeaderMenu-link--sign-in").with_(
        timeout=browser.config.timeout * 4
    ).should(be.visible).click()

    # ASSERT (THEN)
    test_browser.element(".auth-form-header").should(have.text("Sign in to GitHub"))
