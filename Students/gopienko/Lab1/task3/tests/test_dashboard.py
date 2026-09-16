from fastapi.testclient import TestClient

from team_board.main import app


def test_dashboard_starts_and_includes_welcome_dialog() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Подготовить макет" in response.text
    assert 'id="welcome-dialog"' in response.text
