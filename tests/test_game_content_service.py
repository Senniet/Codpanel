from app.services.game_content_service import GameContentService


def test_get_maps_returns_empty_list_for_empty_directory(tmp_path):
    server_path = tmp_path / "server"
    maps_dir = server_path / "main" / "maps"
    maps_dir.mkdir(parents=True)

    assert GameContentService.get_maps(server_path) == []


def test_get_maps_returns_empty_list_for_missing_directory(tmp_path):
    server_path = tmp_path / "server"

    assert GameContentService.get_maps(server_path) == []


def test_get_maps_returns_valid_bsp_files(tmp_path):
    server_path = tmp_path / "server"
    maps_dir = server_path / "main" / "maps"
    maps_dir.mkdir(parents=True)
    (maps_dir / "mp_alpha.bsp").write_text("", encoding="utf-8")
    (maps_dir / "mp_beta.BSP").write_text("", encoding="utf-8")

    assert GameContentService.get_maps(server_path) == ["mp_alpha", "mp_beta"]


def test_get_maps_ignores_non_bsp_files(tmp_path):
    server_path = tmp_path / "server"
    maps_dir = server_path / "main" / "maps"
    maps_dir.mkdir(parents=True)
    (maps_dir / "mp_alpha.bsp").write_text("", encoding="utf-8")
    (maps_dir / "readme.txt").write_text("", encoding="utf-8")
    (maps_dir / "mp_beta.pk3").write_text("", encoding="utf-8")
    (maps_dir / "nested").mkdir()

    assert GameContentService.get_maps(server_path) == ["mp_alpha"]


def test_get_maps_sorts_results_alphabetically(tmp_path):
    server_path = tmp_path / "server"
    maps_dir = server_path / "main" / "maps"
    maps_dir.mkdir(parents=True)
    for name in ("mp_zulu.bsp", "mp_alpha.bsp", "mp_delta.bsp"):
        (maps_dir / name).write_text("", encoding="utf-8")

    assert GameContentService.get_maps(server_path) == [
        "mp_alpha",
        "mp_delta",
        "mp_zulu",
    ]
