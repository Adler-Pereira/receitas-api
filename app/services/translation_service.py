from deep_translator import GoogleTranslator

translator_pt = GoogleTranslator(source="en", target="pt")
translator_en = GoogleTranslator(source="pt", target="en")

FIELDS_TO_SKIP_TRANSLATION = {
    "idMeal",
    "strMealThumb",
    "strYoutube",
    "strSource",
    "strImageSource",
    "dateModified"
}

SEPARATOR = "\n<|||>\n"
MAX_CHARS = 4500


def translate_text_to_en(text: str) -> str:
    return translator_en.translate(text)


def translate_meals(data: dict) -> dict:
    meals = data.get("meals", [])

    for meal in meals:
        texts_to_translate = []
        keys_map = []

        for key, value in meal.items():
            if (
                key not in FIELDS_TO_SKIP_TRANSLATION
                and isinstance(value, str)
                and value.strip()
            ):
                texts_to_translate.append(value)
                keys_map.append((meal, key))

        if not texts_to_translate:
            continue

        payload = SEPARATOR.join(texts_to_translate)

        if len(payload) > MAX_CHARS:
            for (meal_ref, key), text in zip(keys_map, texts_to_translate):
                try:
                    meal_ref[key] = translator_pt.translate(text)
                except Exception:
                    meal_ref[key] = text
            continue

        try:
            translated_payload = translator_pt.translate(payload)
            translated_texts = translated_payload.split(SEPARATOR)

            if len(translated_texts) != len(keys_map):
                raise ValueError

            for (meal_ref, key), translated in zip(keys_map, translated_texts):
                meal_ref[key] = translated

        except Exception:
            for (meal_ref, key), text in zip(keys_map, texts_to_translate):
                meal_ref[key] = text

    return {"meals": meals}
