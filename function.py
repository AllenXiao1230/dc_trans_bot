# local_translator.py
import argostranslate.package
import argostranslate.translate
from langdetect import detect
from langdetect import LangDetectException

class LocalTranslator:
    def __init__(self):
        """
        初始化本地翻译器
        需要先安装必要库和语言包
        """
        self.installed_packages = argostranslate.package.get_installed_packages()
        self.supported_languages = {pkg.from_code: pkg.to_code for pkg in self.installed_packages}

    def _install_model(self, from_code, to_code):
        """安装语言包"""
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package = next(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code, 
                available_packages
            )
        )
        argostranslate.package.install_from_path(package.download())

    def detect_language(self, text):
        """语言检测"""
        try:
            return detect(text)
        except LangDetectException:
            return 'un'

    def translate_text(self, text, target_lang):
        """
        执行本地翻译
        :param text: 要翻译的文本
        :param target_lang: 目标语言代码 (zh/en)
        :return: 翻译结果
        """
        source_lang = self.detect_language(text)
        
        # 查找已安装的翻译模型
        translation = next(
            (p for p in self.installed_packages 
             if p.from_code == source_lang and p.to_code == target_lang),
            None
        )
        
        if not translation:
            raise ValueError(f"No translation model installed for {source_lang}->{target_lang}")
            
        return argostranslate.translate.translate(text, source_lang, target_lang)

    def translate_to_chinese_and_english(self, text):
        """
        双语言本地翻译
        :return: 包含检测语言、中文翻译和英文翻译的字典
        """
        result = {
            'detected_language': 'unknown',
            'chinese': None,
            'english': None
        }

        try:
            # 检测语言
            src_lang = self.detect_language(text)
            result['detected_language'] = src_lang

            # 中文翻译处理
            if src_lang != 'zh':
                result['chinese'] = self.translate_text(text, 'zh')
            else:
                result['chinese'] = text

            # 英文翻译处理
            if src_lang != 'en':
                result['english'] = self.translate_text(text, 'en')
            else:
                result['english'] = text

        except Exception as e:
            print(f"Translation error: {str(e)}")
            
        return result