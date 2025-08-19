from typing import Optional, Union
from bidi.algorithm import get_display, get_base_level

StrOrBytes = Union[str, bytes]

def get_display_wrapper(
    str_or_bytes: StrOrBytes,
    encoding: str = "utf-8",
    base_dir: Optional[str] = None,
    debug: bool = False,
) -> StrOrBytes:
    """
    Accepts string or bytes. Returns display layout.
    - If input is bytes, it will be decoded using `encoding`.
    - If `base_dir` is 'L' or 'R', it sets base level override.
    - `debug=True` returns display layout with extra debug info (handled by python-bidi).
    """
    if isinstance(str_or_bytes, bytes):
        text = str_or_bytes.decode(encoding)
        was_bytes = True
    else:
        text = str_or_bytes
        was_bytes = False

    # Apply python-bidi's get_display
    if base_dir in ("L", "R"):
        # Override base level (0 = LTR, 1 = RTL)
        base_level = 0 if base_dir == "L" else 1
        display = get_display(text, base_dir=base_level)
    else:
        display = get_display(text)

    if was_bytes:
        display = display.encode(encoding)

    return display

def get_base_level_wrapper(text: str) -> int:
    """
    Returns the base unicode level of the first paragraph in `text`.
    0 = LTR, 1 = RTL
    """
    return get_base_level(text)
