# DictedType in LangChain

## Definition

DictedType is a type hint in LangChain that allows you to define a dictionary with a fixed set of string keys, each with a specific value type. This enhances code clarity and helps prevent bugs by enabling static type checkers to validate your dictionary usage.

In LangChain, DictedType is essentially an alias for Python's `TypedDict`, providing a way to create structured, type-safe dictionaries that are commonly used for configuration, data validation, and structured responses.

## Example

```python
from langchain_core.pydantic_v1 import BaseModel
from typing import TypedDict, NotRequired, Required

# Define a TypedDict for user profile data
class UserProfile(TypedDict):
    name: str
    age: int
    email: str
    phone: NotRequired[str]  # Optional field
    address: NotRequired[str]  # Optional field

# Define a TypedDict with all fields optional by default
class ConfigOptions(TypedDict, total=False):
    timeout: int
    retries: int
    debug: Required[bool]  # This field is still required
```

## Code

```python
from langchain_core.pydantic_v1 import BaseModel
from typing import TypedDict, NotRequired, Required

# Basic TypedDict definition
class DocumentMetadata(TypedDict):
    title: str
    author: str
    date_published: str
    tags: list[str]
    word_count: int

# TypedDict with optional fields
class SearchFilters(TypedDict, total=False):
    category: str
    date_range: tuple[str, str]
    min_rating: float
    max_price: Required[float]  # Required even when total=False

# Usage in LangChain context
def process_document(metadata: DocumentMetadata) -> str:
    return f"Processing {metadata['title']} by {metadata['author']}"

def apply_filters(filters: SearchFilters) -> list:
    # filters['category'] might not exist due to total=False
    if 'category' in filters:
        print(f"Filtering by category: {filters['category']}")
    
    # filters['max_price'] is guaranteed to exist
    print(f"Max price: {filters['max_price']}")
    
    return []

# Example usage
doc_meta: DocumentMetadata = {
    "title": "LangChain Tutorial",
    "author": "AI Developer",
    "date_published": "2024-01-15",
    "tags": ["AI", "LangChain", "Python"],
    "word_count": 1500
}

search_opts: SearchFilters = {
    "max_price": 99.99,
    "category": "Technology"
}

# Process the document
result = process_document(doc_meta)
print(result)

# Apply search filters
filtered_results = apply_filters(search_opts)
```

## Explanation

### Key Concepts

1. **Type Safety**: DictedType/TypedDict provides compile-time type checking, helping catch errors before runtime.

2. **Class-based Syntax**: The preferred method is using a class-based syntax where you define keys and their types as class attributes that inherit from TypedDict.

3. **Optional Fields**: You can make fields optional using `NotRequired` for individual keys or by setting `total=False` in the class definition to make all fields optional by default.

4. **Required Fields**: If you've set `total=False`, you can still make specific keys required by using `Required`.

5. **Runtime Behavior**: At runtime, a TypedDict behaves exactly like a regular Python dictionary. The main benefit comes from static analysis tools that use these type hints during development.

### Benefits in LangChain

- **Configuration Management**: Define structured configurations for LangChain components
- **Data Validation**: Ensure data passed between components has the correct structure
- **API Responses**: Type-safe handling of structured responses from language models
- **Document Processing**: Structured metadata for documents and embeddings
- **Tool Definitions**: Type-safe parameter definitions for LangChain tools

### Best Practices

- Use descriptive names for your TypedDict classes
- Keep the structure simple and focused
- Use `NotRequired` sparingly and document why fields are optional
- Consider using `total=False` when most fields are optional
- Use `Required` to override `total=False` for critical fields
