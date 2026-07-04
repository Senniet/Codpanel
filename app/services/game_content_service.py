from pathlib import Path


class GameContentService:
    """Service for discovering and managing game content."""

    @staticmethod
    def get_maps(server_path: Path) -> list[str]:
        """
        Discover available maps from the server directory.

        Scans the main/maps directory within the server path and returns
        all .bsp map filenames without the extension, sorted alphabetically.

        Args:
            server_path: Path to the server directory.

        Returns:
            List of map names (sorted), or empty list if directory does not exist.
        """
        maps_dir = Path(server_path) / "main" / "maps"

        if not maps_dir.exists():
            return []

        maps = [
            f.stem
            for f in maps_dir.iterdir()
            if f.is_file() and f.suffix.lower() == ".bsp"
        ]

        return sorted(maps)
