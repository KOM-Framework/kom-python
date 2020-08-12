"""
https://stackoverflow.com/questions/45028747/suggested-naming-conventions-for-selenium-identifiers

+----------+----------------------------+--------+-----------------+
| Category |      UI/Control type       | Prefix |     Example     |
+----------+----------------------------+--------+-----------------+
| Basic    | Button                     | btn    | btnExit         |
| Basic    | Check box                  | chk    | chkReadOnly     |
| Basic    | Combo box                  | cbo    | cboEnglish      |
| Basic    | Common dialog              | dlg    | dlgFileOpen     |
| Basic    | Date picker                | dtp    | dtpPublished    |
| Basic    | Dropdown List / Select tag | ddl    | ddlCountry      |
| Basic    | Form                       | frm    | frmEntry        |
| Basic    | Frame                      | fra    | fraLanguage     |
| Basic    | Image                      | img    | imgIcon         |
| Basic    | Label                      | lbl    | lblHelpMessage  |
| Basic    | Links/Anchor Tags          | lnk    | lnkForgotPwd    |
| Basic    | List box                   | lst    | lstPolicyCodes  |
| Basic    | Menu                       | mnu    | mnuFileOpen     |
| Basic    | Radio button / group       | rdo    | rdoGender       |
| Basic    | RichTextBox                | rtf    | rtfReport       |
| Basic    | Table                      | tbl    | tblCustomer     |
| Basic    | TabStrip                   | tab    | tabOptions      |
| Basic    | Text Area                  | txa    | txaDescription  |
| Basic    | Text box                   | txt    | txtLastName     |
| Complex  | Chevron                    | chv    | chvProtocol     |
| Complex  | Data grid                  | dgd    | dgdTitles       |
| Complex  | Data list                  | dbl    | dblPublisher    |
| Complex  | Directory list box         | dir    | dirSource       |
| Complex  | Drive list box             | drv    | drvTarget       |
| Complex  | File list box              | fil    | filSource       |
| Complex  | Panel/Fieldset             | pnl    | pnlGroup        |
| Complex  | ProgressBar                | prg    | prgLoadFile     |
| Complex  | Slider                     | sld    | sldScale        |
| Complex  | Spinner                    | spn    | spnPages        |
| Complex  | StatusBar                  | sta    | staDateTime     |
| Complex  | Timer                      | tmr    | tmrAlarm        |
| Complex  | Toolbar                    | tlb    | tlbActions      |
| Complex  | TreeView                   | tre    | treOrganization |
+----------+----------------------------+--------+-----------------+
"""
from typing import Iterable

from selenium.webdriver.common.by import By


class Locator(Iterable):

    def __iter__(self):
        yield self.by
        yield self.value

    def __init__(self, by, value):
        self.by = by
        self.value = value

    def __repr__(self):
        return "%s: %s" % (self.by, self.value)


class Id(Locator):

    def __init__(self, value):
        super().__init__(By.ID, value)


class Xpath(Locator):

    def __init__(self, value):
        super().__init__(By.XPATH, value)


class LinkText(Locator):

    def __init__(self, value):
        super().__init__(By.LINK_TEXT, value)


class PartialLinkText(Locator):

    def __init__(self, value):
        super().__init__(By.PARTIAL_LINK_TEXT, value)


class Name(Locator):

    def __init__(self, value):
        super().__init__(By.NAME, value)


class TagName(Locator):

    def __init__(self, value):
        super().__init__(By.TAG_NAME, value)


class ClassName(Locator):

    def __init__(self, value):
        super().__init__(By.CLASS_NAME, value)


class CssSelector(Locator):

    def __init__(self, value):
        super().__init__(By.CSS_SELECTOR, value)
