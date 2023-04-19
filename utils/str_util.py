from typing import Dict

def facts_to_str(user_data: Dict[str, str]) -> str:
    """
        Formata as escolhas em formato de lista.
    """
    url_filters = {  key.lower().replace(" ", "_"):value for key, value in user_data.items()}
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])