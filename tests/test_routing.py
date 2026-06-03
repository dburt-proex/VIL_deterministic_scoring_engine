from app.core.models import Route
from app.core.routing import route_signal


def test_pass_route():
    assert route_signal(8.0, []) == Route.PASS


def test_review_route():
    assert route_signal(5.5, []) == Route.REVIEW


def test_clarify_route():
    assert route_signal(3.2, []) == Route.CLARIFY


def test_archive_route():
    assert route_signal(1.2, []) == Route.ARCHIVE


def test_halt_overrides_score():
    assert route_signal(9.5, ["policy_violation"]) == Route.HALT
