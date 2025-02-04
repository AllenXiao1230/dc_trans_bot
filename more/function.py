from deep_translator import GoogleTranslator

def translate_text(text):
    try:
        # 自動偵測語言並翻譯
        translated_zh = GoogleTranslator(source='auto', target='zh-CN').translate(text)
        translated_en = GoogleTranslator(source='auto', target='en').translate(text)
        translated_es = GoogleTranslator(source='auto', target='es').translate(text)
        
        return {
            "original": text,
            "chinese": translated_zh,
            "english": translated_en,
            "spanish": translated_es
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}

# 測試
# if __name__ == "__main__":
#     sample_text = "Bonjour tout le monde"
#     result = translate_text(sample_text)
#     print(result)
