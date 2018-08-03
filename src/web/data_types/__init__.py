from collections import Iterable

from selenium.webdriver.common.by import By

from kom_framework import js_waiter_file

with open(js_waiter_file, 'r') as content:
    js_waiter = content.read()


'''
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
'''


class Locator(Iterable):

    def __iter__(self):
        pass

    def __new__(cls, value):
        pass


class Id(Locator):

    def __new__(cls, value):
        return By.ID, value


class Xpath(Locator):

    def __new__(cls, value):
        return By.XPATH, value


class LinkText(Locator):

    def __new__(cls, value):
        return By.LINK_TEXT, value


class PartialLinkText(Locator):

    def __new__(cls, value):
        return By.PARTIAL_LINK_TEXT, value


class Name(Locator):

    def __new__(cls, value):
        return By.NAME, value


class TagName(Locator):

    def __new__(cls, value):
        return By.TAG_NAME, value


class ClassName(Locator):

    def __new__(cls, value):
        return By.CLASS_NAME, value


class CssSelector(Locator):

    def __new__(cls, value):
        return By.CSS_SELECTOR, value
