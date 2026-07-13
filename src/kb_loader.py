FIELD_ORDER = ["title", "pattern", "coreIdea", "recognitionCues", "approach", "techniques", "tags"]
FIELD_LABELS = {
    "title": "Title",
    "pattern": "Pattern",
    "coreIdea": "Core Idea",
    "recognitionCues": "Recognition Cues",
    "approach": "Approach",
    "techniques": "Techniques",
    "tags": "Tags"
}

def entry_to_text(entry):
    lines = []
    for key in FIELD_ORDER:
        if key in entry:
            value = entry[key]
            if isinstance(value, list):
                value = ', '.join(value)
            lines.append(f"{FIELD_LABELS[key]}: {value}")
    return '\n'.join(lines)

