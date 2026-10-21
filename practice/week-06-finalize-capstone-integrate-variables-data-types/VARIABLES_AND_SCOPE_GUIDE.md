# Engineering Guide: Python Variables, Data Types & Scope Architecture

> **Repository**: [parth-mehta95/sahkaarx-stage-portfolio-d5b2372f](https://github.com/parth-mehta95/sahkaarx-stage-portfolio-d5b2372f)  
> **Module**: [`src/variables_data_types.py`](../../src/variables_data_types.py)  
> **Topic**: Variables, Data Types, Memory Model, Type Conversions & LEGB Scope Resolution  

---

## 1. Python Variable Model & Memory Semantics

In Python, variables are **named references (pointers)** bound to objects in heap memory. Understanding the distinction between variables, objects, and references is fundamental to writing high-performance, bug-free applications.

### 1.1 Object Identity, Type, and Value
Every object in Python possesses three critical properties:
1. **Identity (`id()`)**: An integer representing the object's unique memory address during its lifecycle.
2. **Type (`type()`)**: The class defining the object's supported operations, attributes, and internal representation.
3. **Value**: The state data encapsulated by the object.

```text
Variable Name ('x') ──[Reference / Pointer]──> Heap Object:
                                              ├── Identity: 0x7fff34a1b020
                                              ├── Type:     <class 'int'>
                                              ├── RefCount: 1
                                              └── Value:    42
```

### 1.2 Mutability vs. Immutability
Python types are divided into mutable and immutable categories:
- **Immutable Types**: `int`, `float`, `bool`, `str`, `tuple`, `frozenset`, `bytes`. Modifying an immutable value creates a new object in memory.
- **Mutable Types**: `list`, `dict`, `set`, `bytearray`, custom user objects. In-place mutations modify the object in-place without altering its memory identity.

```python
# Modifying immutable creates a new object
x = 10
old_id = id(x)
x += 1
assert id(x) != old_id  # New memory location!

# Mutating mutable preserves identity
arr = [1, 2]
old_arr_id = id(arr)
arr.append(3)
assert id(arr) == old_arr_id  # Same memory location!
```

---

## 2. Type Conversion: Implicit vs. Explicit

Type conversion (casting) transfers data from one type representation to another.

### 2.1 Implicit Type Coercion
Python automatically coerces types during mixed-mode arithmetic to prevent data loss:
- `int + float -> float`: `5 + 2.5 -> 7.5`
- `bool + int -> int`: `True + 3 -> 4`
- `int + Decimal -> TypeError`: Python refuses implicit conversion between binary floats/ints and `Decimal` to enforce explicit numeric precision boundaries.

### 2.2 Explicit Conversion Mechanics
Explicit conversions invoke type constructors or conversion protocols (`__int__`, `__float__`, `__str__`):

| Target Type | Constructor | Behavior & Edge Cases |
| :--- | :--- | :--- |
| **`int`** | `int(x)` | Truncates float toward zero (`int(4.9) -> 4`). Parses numeric strings. Throws `ValueError` on fractional strings (`int("4.9")` fails). |
| **`float`** | `float(x)` | Converts integers, strings, and scientific notation (`"1e3"`). May introduce IEEE 754 precision artifacts. |
| **`Decimal`** | `Decimal(str(x))` | Exact base-10 arithmetic. Always convert floats through string representation (`Decimal(str(0.1))`) to prevent roundoff errors. |
| **`bool`** | `bool(x)` | Evaluates truthiness. Zero, empty containers (`[]`, `{}`, `""`), and `None` evaluate to `False`; all other values evaluate to `True`. |
| **`tuple`** | `tuple(x)` | Converts any iterable to an immutable sequence. |
| **`frozenset`** | `frozenset(x)` | Deduplicates iterable elements into an immutable, hashable set. |

---

## 3. Variable Scope Architecture: The LEGB Rule

Python searches for variable names hierarchically according to the **LEGB Rule**:

```text
+-------------------------------------------------------------------+
|  1. Local (L)                                                     |
|     Names defined inside the active function or lambda.           |
|     Search starts here.                                           |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|  2. Enclosing (E)                                                 |
|     Names in the local scope of any enclosing functions           |
|     (from innermost to outermost). Used in nested functions/closures.|
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|  3. Global (G)                                                    |
|     Names defined at the top level of the current module file,    |
|     or explicitly declared with 'global'.                         |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|  4. Built-in (B)                                                  |
|     Built-in functions, exceptions, and constants in builtins     |
|     (e.g., len, range, print, ValueError).                        |
+-------------------------------------------------------------------+
                                  |
                                  v
                        NameError: name 'x' is not defined
```

### 3.1 The `nonlocal` Keyword and Stateful Closures
When an inner function needs to rebind a variable defined in an outer enclosing function, the `nonlocal` keyword is required:

```python
def make_accumulator(start=0):
    total = start  # Enclosing scope variable
    
    def add(n):
        nonlocal total  # Rebinds 'total' in the enclosing frame
        total += n
        return total
        
    return add

acc = make_accumulator(10)
acc(5)   # -> 15
acc(10)  # -> 25
```

### 3.2 The `global` Keyword
To rebind a module-level variable inside a function, declare it with `global`:

```python
GLOBAL_COUNTER = 0

def increment_global():
    global GLOBAL_COUNTER
    GLOBAL_COUNTER += 1
```

> **Best Practice**: Minimize mutable global state. When required, encapsulate within an audited manager class like `ScopeManager.update_global_state()` with defensive copying.

### 3.3 Comprehension Scoping in Python 3
In Python 3, list, dict, and set comprehensions have their own local execution frame, preventing loop iteration variables from leaking into the enclosing namespace:

```python
x = "original"
squares = [x * 2 for x in range(5)]
assert x == "original"  # 'x' is protected from leakage!
```

---

## 4. Immutability & Defensive Programming Best Practices

1. **NamedTuples and Frozen Dataclasses**:
   Use `typing.NamedTuple` or `@dataclass(frozen=True)` for domain entities and configurations to prevent accidental mutation.
2. **Defensive Copies Across Boundaries**:
   Use `copy.deepcopy()` when passing mutable objects across scope boundaries or storing them in shared registries.
3. **Guard Against Shadowing Built-ins**:
   Never name variables `id`, `type`, `list`, `dict`, `str`, `len`, `sum`, or `format`.
4. **Explicit Type Hints**:
   Use PEP 484 and PEP 526 annotations (`Final`, `Optional`, `Union`, `Callable`) to enforce static type contracts and facilitate IDE autocompletion.
