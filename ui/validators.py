# ui/validators.py
"""
Herbruikbare validatie functies voor de UI layer.
Bevat functies voor input validatie, menu keuzes en bevestigingen.
"""

from datetime import datetime
from typing import Optional

# === Validatie Constanten ===
MAX_PROJECT_NAME_LENGTH = 100
MIN_PROJECT_NAME_LENGTH = 2
MAX_DESCRIPTION_LENGTH = 500
MAX_MENU_ATTEMPTS = 3
FORBIDDEN_FILENAME_CHARS = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']


def validate_project_name(name: str) -> tuple[bool, str]:
    """
    Valideert een projectnaam op basis van lengte en verboden karakters.
    
    Args:
        name: De projectnaam om te valideren
    
    Returns:
        Tuple van (is_valid, error_message)
        - is_valid: True als de naam geldig is
        - error_message: Lege string als geldig, anders de foutmelding
    """
    if not name:
        return False, "Naam is verplicht!"
    
    if len(name) < MIN_PROJECT_NAME_LENGTH:
        return False, f"Naam moet minimaal {MIN_PROJECT_NAME_LENGTH} tekens bevatten."
    
    if len(name) > MAX_PROJECT_NAME_LENGTH:
        return False, f"Naam mag maximaal {MAX_PROJECT_NAME_LENGTH} tekens bevatten."
    
    for char in FORBIDDEN_FILENAME_CHARS:
        if char in name:
            return False, f"Naam mag geen '{char}' bevatten."
    
    return True, ""


def validate_description(description: str) -> tuple[bool, str]:
    """
    Valideert een beschrijving op basis van lengte.
    
    Args:
        description: De beschrijving om te valideren
    
    Returns:
        Tuple van (is_valid, error_message)
    """
    if len(description) > MAX_DESCRIPTION_LENGTH:
        return False, f"Beschrijving mag maximaal {MAX_DESCRIPTION_LENGTH} tekens bevatten."
    
    return True, ""


def get_valid_project_id(prompt: str = "Voer project-ID in: ") -> Optional[int]:
    """
    Vraagt om een project-ID met validatie.
    
    Args:
        prompt: De prompt tekst om te tonen
    
    Returns:
        Het project-ID als positief geheel getal, of None bij ongeldige invoer
    """
    user_input = input(prompt).strip()
    
    if not user_input:
        print("⚠️ Geen ID ingevoerd.")
        return None
    
    try:
        proj_id = int(user_input)
        if proj_id <= 0:
            print("⚠️ ID moet een positief getal zijn.")
            return None
        return proj_id
    except ValueError:
        print(f"⚠️ '{user_input}' is geen geldig nummer.")
        return None


def get_menu_choice(prompt: str, valid_options: list[str], max_attempts: int = MAX_MENU_ATTEMPTS) -> Optional[str]:
    """
    Vraagt om een menu keuze met validatie en retry logica.
    
    Args:
        prompt: De prompt tekst om te tonen
        valid_options: Lijst van geldige opties (bv. ["1", "2", "3"])
        max_attempts: Maximum aantal pogingen (standaard: MAX_MENU_ATTEMPTS)
    
    Returns:
        De gekozen optie als string, of None na max_attempts ongeldige pogingen
    
    Example:
        >>> choice = get_menu_choice("Kies optie (1-3): ", ["1", "2", "3"])
        >>> if choice == "1":
        ...     do_something()
    """
    for attempt in range(max_attempts):
        choice = input(prompt).strip()
        if choice in valid_options:
            return choice
        
        remaining = max_attempts - attempt - 1
        if remaining > 0:
            print(f"⚠️ Ongeldige keuze. Nog {remaining} poging(en).")
    
    print("❌ Te veel ongeldige pogingen.")
    return None


def confirm_action(prompt: str, default: bool = False) -> bool:
    """
    Vraagt om bevestiging met duidelijke ja/nee opties.
    
    Args:
        prompt: De vraag tekst (zonder ja/nee hint)
        default: Standaard antwoord bij lege input (False = nee, True = ja)
    
    Returns:
        True voor ja, False voor nee
    
    Example:
        >>> if confirm_action("Wil je doorgaan?"):
        ...     print("Doorgaan...")
        >>> if confirm_action("Wil je verwijderen?", default=False):
        ...     delete_item()
    """
    default_hint = "(J/n)" if default else "(j/N)"
    response = input(f"{prompt} {default_hint}: ").strip().lower()
    
    if not response:
        return default
    
    return response in ("j", "ja", "y", "yes")


def parse_datetime(input_str: str, format: str = "%d/%m/%Y %H:%M") -> Optional[datetime]:
    """
    Parseert een datum/tijd string met validatie.
    
    Args:
        input_str: De datum/tijd string om te parsen
        format: Het verwachte formaat (standaard: "dd/mm/yyyy HH:MM")
    
    Returns:
        Een datetime object, of None bij ongeldige invoer
    
    Example:
        >>> dt = parse_datetime("25/12/2024 14:30")
        >>> if dt:
        ...     print(f"Datum: {dt}")
    """
    try:
        return datetime.strptime(input_str.strip(), format)
    except ValueError:
        print(f"⚠️ Ongeldige datum/tijd. Gebruik formaat: {format}")
        return None


def get_non_empty_input(prompt: str, field_name: str = "Invoer") -> Optional[str]:
    """
    Vraagt om niet-lege invoer.
    
    Args:
        prompt: De prompt tekst om te tonen
        field_name: Naam van het veld voor de foutmelding
    
    Returns:
        De invoer als string (gestript), of None als leeg
    """
    user_input = input(prompt).strip()
    
    if not user_input:
        print(f"⚠️ {field_name} mag niet leeg zijn.")
        return None
    
    return user_input


def get_optional_input(prompt: str, default: str = "") -> str:
    """
    Vraagt om optionele invoer met een standaardwaarde.
    
    Args:
        prompt: De prompt tekst om te tonen
        default: De standaardwaarde als niets wordt ingevoerd
    
    Returns:
        De invoer als string (gestript), of de default waarde
    """
    user_input = input(prompt).strip()
    return user_input if user_input else default
