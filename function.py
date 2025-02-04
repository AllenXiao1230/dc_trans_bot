from deep_translator import GoogleTranslator

# 所有支援的語言（語言代碼: 語言名稱）
LANGUAGE_NAMES = {
    "zh-TW": "繁體中文",
    "en": "English",
    "es": "Español",
    "ja": "日本語",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
    "ko": "한국語",
    "ru": "Русский",
    "pt": "Português",
    "ar": "العربية",
    "hi": "हिन्दी"
}

# 目前啟用的翻譯語言
active_languages = ["zh-TW", "en", "es", "ja"]

# 翻譯函式
def translate_text(text):
    try:
        results = {}
        for lang in active_languages:
            translated = GoogleTranslator(source='auto', target=lang).translate(text)
            results[lang] = translated

        return "\n".join([f"**{LANGUAGE_NAMES.get(lang, '未知語言')}**: {results[lang]}" for lang in active_languages])
    except Exception as e:
        return f"錯誤: {str(e)}"

# 取得目前啟用 & 可新增的語言清單
def get_language_lists():
    enabled = {lang: LANGUAGE_NAMES.get(lang, "未知語言") for lang in active_languages}
    available = {lang: LANGUAGE_NAMES.get(lang, "未知語言") for lang in LANGUAGE_NAMES if lang not in active_languages}
    return enabled, available

# 新增翻譯語言
def add_language(lang):
    if lang in LANGUAGE_NAMES and lang not in active_languages:
        active_languages.append(lang)
        return f"✅ 已新增語言: {LANGUAGE_NAMES[lang]}"
    return f"⚠️ 語言 {LANGUAGE_NAMES.get(lang, lang)} 已存在或不支援！"

# 刪除翻譯語言
def remove_language(lang):
    if lang in active_languages:
        active_languages.remove(lang)
        return f"❌ 已移除語言: {LANGUAGE_NAMES.get(lang, '未知語言')}"
    return f"⚠️ 語言 {LANGUAGE_NAMES.get(lang, lang)} 不存在於目前的翻譯清單！"
