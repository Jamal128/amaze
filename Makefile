install:
	uv sync --extra dev
	uv pip install ./mlx-2.2-py3-none-any.whl

run:
	uv run python3 a_maze_ing.py config.txt

build:
	uv run python3 -m build
	cp ./dist/mazegen-1.0.0-py3-none-any.whl .

debug:
	uv run python3 -m pdb a_maze_ing.py default_config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf dist build *.egg-info

lint:
	uv run flake8 --exclude=.venv,mlx .
	uv run python3 -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--explicit-package-bases \
		--exclude '^(venv|\.venv|env|mlx)/'

lint-strict:
	uv run flake8 --exclude=.venv,mlx .
	uv run python3 -m mypy . \
		--strict \
		--explicit-package-bases \
		--exclude '^(venv|\.venv|env|mlx)/'