from typing import Optional, Tuple
from pydantic import BaseModel, Field, field_validator, model_validator


class Coordinates(BaseModel):
    '''Modelo para representar coordenadas (x, y) en el laberinto.
        x: Horizontal position (column index).
        y: Vertical position (row index).
    '''
    x: int
    y: int
    def __str__(self) -> str:
        return f"{self.x},{self.y}"
    def return_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)


class MazeConfig(BaseModel):
    """Configuration model for the maze generator.

    Attributes:
        width: Number of columns in the maze. Must be >= 2.
        height: Number of rows in the maze. Must be >= 2.
        entry: Entry cell coordinates.
        exit_: Exit cell coordinates.
        output_file: Path to the output file.
        perfect: Whether the maze must be perfect (single path).
        seed: Optional seed for reproducibility.
        algorithm: Optional name of the generation algorithm.
    """
    width: int = Field(..., alias="WIDTH", ge=2, description="Maze width")
    height: int = Field(..., alias="HEIGHT", ge=2, description="Maze height")
    entry: Coordinates = Field(..., alias="ENTRY")
    exit_: Coordinates = Field(..., alias="EXIT")
    output_file: str = Field(..., alias="OUTPUT_FILE")
    perfect: bool = Field(..., alias="PERFECT")
    seed: Optional[int] = Field(default=None, alias="SEED")
    algorithm: Optional[str] = Field(default=None, alias="ALGORITHM")

    model_config = {"populate_by_name": True}

    @field_validator("entry", "exit_", mode="before")
    @classmethod
    def parse_coordinates(cls, value: object) -> Coordinates:
        """Parse 'x,y' string into a Coordinates model.

        Args:
            value: Raw coordinate string, e.g. '0,0' or '19,14'.

        Returns:
            A Coordinates instance.

        Raises:
            ValueError: If the string format is invalid.
        """
        if isinstance(value, Coordinates):
            return value
        parts = [p.strip() for p in value.split(",")]
        if len(parts) != 2:
            raise ValueError(f"Got Invalid Coors: {value!r} expected: (x, y).")
        try:
            x = int(parts[0])
            y = int(parts[1])
        except ValueError as e:
            raise ValueError(f"Invalid coordinate: {value!r} "
                             f"(x, y must be integers).") from e
        return Coordinates(x=x, y=y)

    @field_validator("perfect", mode="before")
    @classmethod
    def parse_bool(cls, value: object) -> bool:
        if isinstance(value, bool):
            return value
        val = value.strip().lower()
        if val in {"true", "1", "yes", "y"}:
            return True
        if val in {"false", "0", "no", "n"}:
            return False
        raise ValueError(f"Invalid: {value!r} expected: True/False.")

    @field_validator("seed", mode="before")
    @classmethod
    def parse_optional_int(cls, value: object) -> Optional[int]:
        """Parse an optional integer field.

        Args:
            value: Raw value or None.

        Returns:
            Parsed integer or None.
        """
        if value is None or str(value).strip() == "":
            return None
        try:
            return int(str(value).strip())
        except (ValueError, TypeError) as exc:
            raise ValueError("SEED must be an integer") from exc

    @model_validator(mode="after")
    def validate_bounds(self) -> "MazeConfig":
        """Ensure entry and exit coordinates are within maze bounds.

        Returns:
            The validated MazeConfig instance.

        Raises:
            ValueError: If entry or exit are out of bounds, or identical.
        """
        def _check(label: str, coord: Coordinates) -> None:
            if not (0 <= coord.x < self.width):
                raise ValueError(
                    f"{label} x={coord.x} is out of bounds "
                    f"(maze width={self.width})"
                )
            if not (0 <= coord.y < self.height):
                raise ValueError(
                    f"{label} y={coord.y} is out of bounds "
                    f"(maze height={self.height})"
                )

        _check("ENTRY", self.entry)
        _check("EXIT", self.exit_)

        if self.entry.return_tuple() == self.exit_.return_tuple():
            raise ValueError("ENTRY and EXIT must be different cells.")

        return self
