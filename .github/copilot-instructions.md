## General Principles

- Write code that is **readable, maintainable, and well-structured**.
- Follow the **DRY (Don’t Repeat Yourself) principle** to avoid redundancy.
- Use **descriptive variable and function names** in German where appropriate (e.g., `berechne_gewinn_zahlen` instead of `calc_win`).
- Keep code **simple and concise** while ensuring clarity—**avoid over-engineering**.
- Use single quotes for **string literals** unless double quotes are needed inside the string.

## PEP 8 Compliance

- **Indentation:** Use **4 spaces** per indentation level. No tabs.
- **Line Length:** Limit lines to **79 characters**. Use parentheses (not backslashes) for line continuation.
- **Blank Lines:**
  - **2 blank lines** before top-level function and class definitions.
  - **1 blank line** between methods inside a class or logical sections within a function.
- **Whitespace:**
  - Add **one space** after commas (`func(a, b)` not `func(a,b)`).
  - Avoid extra whitespace inside parentheses (`(x + y)` not `( x + y )`).
  - Use spaces around operators (`x = 5 + 3` not `x=5+3`).
- **Naming Conventions:**
  - **Functions & variables:** `snake_case` (e.g., `get_user_data`).
  - **Classes:** `PascalCase` (e.g., `DataProcessor`).
  - **Constants:** `UPPER_CASE` (e.g., `MAX_RETRIES`).
  - **Avoid** single-letter variable names except in short loops (`for i in range(5)`).

## Code Structure

- **Imports:** Place imports at the **top** in this order:
  1. **Standard library** (e.g., `import os`)
  2. **Third-party libraries** (e.g., `import numpy as np`)
  3. **Local application modules** (e.g., `from my_module import my_function`)
  - Use **one import per line**; avoid `from module import *`.
  - **Sort imports alphabetically** within each group.
  - **Remove** unused libraries **in the import functions** to keep code clean.
- **Main Block:** Use `if __name__ == "__main__":` to prevent code from running on import.
- **Functions:**
  - Include a **docstring** explaining purpose, parameters, and return value:
    ```python
    def calculate_area(radius: float) -> float:
        """Calculate the area of a circle given the radius."""
        return 3.1416 * radius ** 2
    ```
  - Keep functions **focused**—do **one thing well**.
  - Limit function length to **20–30 lines** where possible.
- **Classes:**
  - Use **classes** when data and behavior are closely related.
  - Include an **`__init__` method** with **clear parameter names**.
  - Add a **class-level docstring** explaining its purpose.

## Type Hints

- Use **type hints** to improve clarity:

  ```python
  from typing import List, Union

  def add_numbers(a: int, b: int) -> int:
      """Add two integers and return the sum."""
      return a + b

  def get_items_list(items: List[Union[str, int]]) -> List[str]:
      """Convert all items to strings and return the new list."""
      return [str(item) for item in items]
  ```

- Annotate **both parameters and return types**.
- Consider using **Optional** for nullable parameters, and **Any** when type is unspecified.

## Error Handling

- Use `try/except` blocks to handle exceptions gracefully.
- Catch **specific exceptions** (e.g., `ValueError`) rather than generic ones.
- Include **meaningful error messages** or **log** them:
  ```python
  try:
      value = int(input("Enter a number: "))
  except ValueError:
      print("Invalid input! Please enter an integer.")
  ```

## Comments

- **Explain why**, not just **what**:
  ```python
  # Adjust threshold to avoid false positives
  threshold = 0.8
  ```
- Keep comments **concise and relevant**.
- Avoid **redundant** comments (e.g., `# Set x to 5` above `x = 5`).
- Use **inline comments sparingly** and align them.

## Code Output Formatting

- Wrap code in **triple backticks** specifying the language:
  ```python
  def example_function():
      """Example function."""
      pass
  ```
- If multiple snippets are needed, separate them with **descriptive headings** and add brief explanations before or after each snippet.

## Additional Best Practices

- **Avoid global variables**—pass data via parameters.
- Use **list comprehensions** or **generators** for concise, readable iteration:
  ```python
  squares = [x**2 for x in range(10)]
  ```
- Test **edge cases** mentally and mention them in your explanation if they’re critical.
- Use **logging** instead of `print()` in production-level code:

  ```python
  import logging

  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  logger.info("Starting process...")
  ```

# Lottery Analysis Platform - Coding Guidelines

## Project-Specific Standards

### Lottery Data Handling

```python
from datetime import datetime
from typing import List, Dict, Optional

class LottoZiehung:
    """Represents a single lottery draw with validation and analysis capabilities."""

    def __init__(
        self,
        ziehung_datum: datetime,
        gewinn_zahlen: List[int],
        superzahl: Optional[int] = None
    ):
        """Initialize a lottery draw instance.

        Args:
            ziehung_datum: Date and time of the draw
            gewinn_zahlen: List of drawn numbers
            superzahl: Optional super number
        """
        self.validate_numbers(gewinn_zahlen)
        self.ziehung_datum = ziehung_datum
        self.gewinn_zahlen = sorted(gewinn_zahlen)
        self.superzahl = superzahl

    @staticmethod
    def validate_numbers(numbers: List[int]) -> None:
        """Validate lottery numbers according to game rules."""
        if not all(1 <= n <= 49 for n in numbers):
            raise ValueError("Zahlen müssen zwischen 1 und 49 liegen")
```

### Analysis Implementation

```python
class ZahlenAnalyse:
    """Base class for number analysis implementations."""

    def __init__(self, zeitraum_tage: int = 30):
        """Initialize analysis with time period.

        Args:
            zeitraum_tage: Analysis period in days
        """
        self.zeitraum_tage = zeitraum_tage
        self._cache = {}  # Internal cache for analysis results

    def analysiere_haeufigkeit(self) -> Dict[int, int]:
        """Analyze number frequency within the specified period."""
        pass
```

## Code Structure

### Project Layout

- Place lottery system-specific code in dedicated modules (e.g., `lotto6aus49/`)
- Keep analysis utilities separate from data models
- Use appropriate caching mechanisms for analysis results

### Imports Organization

```python
# Standard library
from datetime import datetime
from typing import List, Dict

# Third-party packages
import numpy as np
from sqlalchemy import Column, Integer

# Local application imports
from lotto6aus49.models import LottoZiehung
from common.utils import cache_result
```

### Error Handling

```python
class LottoAnalyseError(Exception):
    """Base exception for lottery analysis errors."""
    pass

try:
    zahlen = analyse.get_haeufige_zahlen()
except LottoAnalyseError as e:
    logger.error(f"Analyse fehlgeschlagen: {str(e)}")
    raise
```

## Documentation

### Function Documentation

```python
def analysiere_muster(
    ziehungen: List[Dict[str, any]],
    zeitfenster: int = 10
) -> Dict[str, any]:
    """Analyze pattern frequencies in lottery draws.

    Args:
        ziehungen: List of historical draws
        zeitfenster: Time window for analysis in days

    Returns:
        Dictionary containing pattern analysis results

    Raises:
        LottoAnalyseError: If analysis fails
    """
    pass
```

## Performance Guidelines

### Caching Strategy

```python
from functools import lru_cache
from redis import Redis

redis = Redis(host='localhost', port=6379, db=0)

@lru_cache(maxsize=100)
def get_ziehungs_analyse(ziehung_id: int) -> Dict[str, any]:
    """Get cached analysis for a specific draw."""
    cache_key = f"analyse:{ziehung_id}"
    return redis.get(cache_key)
```

### Database Operations

```python
from sqlalchemy.orm import Session
from typing import List, Dict

def bulk_insert_ziehungen(ziehungen: List[Dict]) -> None:
    """Efficiently insert multiple draws using bulk operations."""
    with Session() as session:
        session.bulk_insert_mappings(LottoZiehung, ziehungen)
        session.commit()
```

## Testing

```python
def test_ziehungs_validierung():
    """Test lottery draw number validation."""
    with pytest.raises(ValueError, match="Zahlen müssen zwischen 1 und 49 liegen"):
        LottoZiehung(
            ziehung_datum=datetime.now(),
            gewinn_zahlen=[0, 50, 25]  # Invalid numbers
        )
```

## Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Use meaningful log messages in German
logger.info("Starte Analyse der Lottozahlen...")
logger.error("Fehler bei der Datenverarbeitung: %s", str(error))
```

