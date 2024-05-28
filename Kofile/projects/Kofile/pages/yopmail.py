"""
yopmail.com Page Object Model
"""
from projects.Kofile.Lib.test_parent import PagesParent


class YOPMail(PagesParent):
    def __init__(self):
        super(YOPMail, self).__init__()

    login_input_xpath = ("xpath", '//*[@id="login"]', "Login input")
    login_btn_xpath = ("xpath", '//*[@id="refreshbut"]', "Login button")
    email_row_xpath = ("xpath", '(//*[@class="lm"])[1]', "Email first row")
    attached_pdf_xpath = ("xpath", '//*[@class="fl pjs yscrollbar"]/a', "Attached PDF")
    attached_pdf_name_xpath = ("xpath", '//*[@class="fl pjs yscrollbar"]/descendant::span', "Attached PDF name")


