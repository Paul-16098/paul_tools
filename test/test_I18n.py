from .__init__ import *


# @unittest.skip("")
class I18nTest(unittest.TestCase):
    def test_locale(self):
        from ..I18n import I18n
        import locale
        default_locale_code = str(locale.getdefaultlocale()[0]).lower()
        current_locale_description = str(
            locale.getlocale(locale.LC_CTYPE)[0]).lower()

        default_locale_code = I18n.langReplace(default_locale_code)
        current_locale_description = I18n.langReplace(
            current_locale_description)

        # 你可以根據需要調整這裡的斷言
        self.assertEqual(default_locale_code,
                         current_locale_description)
