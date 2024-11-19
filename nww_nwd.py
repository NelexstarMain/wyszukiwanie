from typing import Optional, Union, Callable, Dict, Tuple, List
from functools import wraps

def validate_numbers(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(a: Union[int, float], b: Union[int, float]) -> int:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Argumenty muszą być liczbami")
        return func(round(float(a)), round(float(b)))
    return wrapper

@validate_numbers
def nwd(a: Union[int, float], b: Union[int, float]) -> int:
    if a == 0 and b == 0:
        raise ValueError("Przynajmniej jedna z liczb musi być różna od zera")
    
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return int(a)

@validate_numbers
def nww(a: Union[int, float], b: Union[int, float]) -> int:
    if a == 0 and b == 0:
        raise ValueError("Przynajmniej jedna z liczb musi być różna od zera")
    
    return abs(int(a * b)) // nwd(a, b)

def calculate(
    a: Optional[Union[int, float]] = None, 
    b: Optional[Union[int, float]] = None, 
    action: str = "nww"
) -> Optional[Union[int, str]]:
    functions: Dict[str, Callable] = {
        "nww": nww,
        "nwd": nwd
    }
    
    if action not in functions:
        return None
        
    x = 10 if a is None else a
    y = 10 if b is None else b
    
    try:
        return functions[action](x, y)
    except Exception as e:
        return str(e)

def parse_input(text: str) -> Tuple[List[Union[int, float]], str]:
    try:
        parts = text.split()
        if len(parts) != 3:
            raise IndexError("Wymagane są dokładnie 3 argumenty: <a> <b> <action>")
        
        arguments = [float(x) for x in parts[:2]]
        action = parts[2].lower()
        
        if action not in ("nwd", "nww"):
            raise ValueError("Akcja musi być 'nwd' lub 'nww'")
            
        return arguments, action
    except ValueError as e:
        raise ValueError("Nieprawidłowy format liczb") from e

def main() -> None:
    while True:
        try:
            text = input("Podaj <a> <b> <action> (lub 'q' aby zakończyć): ")
            if text.lower() == 'q':
                break
                
            arguments, action = parse_input(text)
            result = calculate(*arguments, action)
            print(f"Wynik: {result}")
            
        except (ValueError, IndexError) as e:
            print(f"Błąd: {e}")
        except KeyboardInterrupt:
            print("\nProgram zakończony.")
            break

if __name__ == "__main__":
    main()