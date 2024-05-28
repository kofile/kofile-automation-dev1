"""
General purpose Page Object Model helpers
"""
import logging
import os
import random
import string
import time
from datetime import datetime

from golem import actions
from golem.browser import element
from psutil import process_iter, AccessDenied
from pytz import timezone
from selenium.common.exceptions import ElementNotVisibleException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

scroll_js = 'arguments[0].scrollIntoView();'
min_year = 1901
DATE_PATTERN = r"%m/%d/%Y"
TIMEZONE = "Canada/Central"
strings_dict = {0: string.ascii_letters + string.digits, 4: string.ascii_letters,
                5: string.ascii_letters + r'!@#$%^&*()~`{}[];:"<>?|\/', 1: string.digits, 2: "01"}

JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;
    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };
      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });
      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""


def return_on_failure(value, print_ms=None):
    def decorate(f):
        def applicator(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                logging.log(logging.ERROR, e)
                if print_ms:
                    print(print_ms.format(type(e).__name__))
                return value

        return applicator

    return decorate


def get_url(ind=0, url_arg="url") -> str:
    env = actions.execution.data.get("env")
    user = env.get("user")
    pwd = env.get("password")
    return env.get(url_arg) % (
        (user[ind] if isinstance(user, list) else user,
         pwd[ind] if isinstance(pwd, list) else pwd, env.get("code"), env.get("code")))


class GeneralHelpers:
    """
    General purpose helpers for the whole project
    """
    DATE_PATTERN = r"%m/%d/%Y"
    TIMEZONE = "Canada/Central"

    @staticmethod
    def create_amounts(payments, total_amount: int) -> list:
        payments_count = len(payments)
        left_amount = total_amount
        result = list()
        for n, _ in enumerate(payments):
            if n == payments_count - 1:
                result.append(round(left_amount, 2))
            else:
                new_amount = round(left_amount / 2, 2)
                left_amount = left_amount - new_amount
                result.append(new_amount)
        assert round(sum(result), 2) == total_amount, f"{round(sum(result), 2)} != {total_amount}"
        return result

    def check_order_type(self):
        data = self.get_data()
        order_types = data['config'].get_order_types()
        if data.OIT not in order_types:
            raise Errors.NoOrderTypeError(f"{data.OIT} does not exist for current tenant")

    @staticmethod
    def reset_focus():
        actions.get_browser().execute_script("!!document.activeElement ? document.activeElement.blur() : 0")

    @staticmethod
    def verify_drop_down_options(loc, text_list: list = None, value_list: list = None, options_count: int = None,
                                 parent=None):
        options = GeneralHelpers.find(loc, parent=parent).find_elements_by_tag_name("option")
        options_value = [i.get_attribute("value") for i in options]
        options_texts = [i.text for i in options]
        if options_count:
            assert len(options) == options_count, f"Select must have {options_count} options, but have {len(options)}"
        if text_list:
            for option in text_list:
                assert option in options_texts, f"Cant find option {option} in dropdown {loc}"
        if value_list:
            for val in value_list:
                assert val in options_value, f"Cant find value {val} in dropdown {loc}"
        return options_texts, options_value

    @staticmethod
    def get_data():
        return actions.execution.data

    @staticmethod
    def add_log(log, log_lvl="INFO"):
        logging.log(logging.ERROR if log_lvl == "ERROR" else logging.INFO, log)

    @staticmethod
    @return_on_failure(None)
    def make_locator(*args):
        """
        formats parameterized POM locator, based on given arguments. returns valid POM tuple

        first argument always has to be parameterized POM locator, the rest of arguments depends on
        number of '%s' in given POM locator. the number of the rest arguments have to be equal
        to the number of '%s' in POM locator.

        example:

        POM locator - '//div[%s]/ul/li[%s]', the number of the rest arguments have to be 2, e.g. '1', '2',
        result - '//div[1]/ul/li[2]'

        in case of exception or invalid number of arguments, returns None
        """
        if (len(args) - 1) == args[0][1].count("%s"):
            return args[0][0], args[0][1] % args[1:], args[0][2]
        raise ValueError("wrong number of arguments")

    @staticmethod
    @return_on_failure(1)
    def scroll_into_view(pom: tuple or element):
        """
        scrolls into view given page object,
        returns 0, if error returns 1

        pom - POM locator
        """
        actions.get_browser().execute_script(scroll_js, actions.get_browser().find(pom) if type(pom) == tuple else pom)
        actions.wait(0.5)
        return 0

    @staticmethod
    def wait_until(some_predicate, timeout, period=0.25, *args, **kwargs):
        must_end = time.time() + timeout
        while time.time() < must_end:
            if some_predicate(*args, **kwargs):
                return True
            time.sleep(period)
        return False

    @staticmethod
    @return_on_failure("")
    def random_string(str_len, str_type=0):
        """returns random alphanumeric, alpha only, alpha w special chars, numeric,
        bit or decimal as string. if error returns empty string

         str_len - string length,
         str_type - return type: 0 - alphanumeric, 1 - numeric, 2 - bit, 3 - decimal
         with 2 decimal digits (str_len includes all digits), 4 - alpha only,
         5 - alpha and special characters"""
        random.seed = os.urandom(str_len)
        if str_type in strings_dict:
            return ''.join(random.choices(strings_dict.get(str_type), k=1 if str_type == 2 else str_len))
        elif str_type == 3 and str_len > 2:
            return "{}.{}".format(''.join(random.choices(string.digits, k=str_len - 2)),
                                  ''.join(random.choices(string.digits, k=2)))
        return ""

    @staticmethod
    def wait_url_change(old_url, timeout=60):
        for __ in range(timeout):
            if actions.get_current_url() != old_url:
                return
            actions.wait(1)
        raise ValueError("Url has not been changed \n{}".format(old_url))

    @staticmethod
    def random_year(ky_ear):
        """returns year as string in a range between 1901 and ky_ear"""
        return str(random.randint(min_year, ky_ear))

    @staticmethod
    @return_on_failure('')
    def random_date(k_year, k_month, k_day, use_today=False):
        """returns date as string in format 'mmddyyyy' earlier (or equal to) than
        k_year-k_month-k_day date and more than min_year = 1901

        if use_today is True, today date is used instead of k_year, k_month, k_day"""
        if use_today:
            return "{}{}{}".format("{:02}".format(datetime.today().month),
                                   "{:02}".format(datetime.today().day),
                                   datetime.today().year)
        new_year = random.randint(min_year, k_year)
        new_month = random.randint(1, k_month)
        new_day = random.randint(1, 25) if k_day > 25 else random.randint(1, k_day)
        return "{:02}".format(new_month) + "{:02}".format(new_day) + str(new_year)

    @staticmethod
    def get_url(ind=0) -> str:
        """
        returns CRS URL for current environment
        """
        return get_url(ind)

    @staticmethod
    def get_ftp_url():
        """
        returns CRS URL for current environment
        """
        env = actions.execution.data.get("env")
        return env.get("ftp") % (env.get("code"))

    @staticmethod
    def get_env_code():
        """
        returns CRS URL for current environment
        """
        env = actions.execution.data.get("env")
        return env.get("code")

    @staticmethod
    def get_env_name():
        """
        returns CRS URL for current environment
        """
        env = actions.execution.data.get("env")
        return env.get("name")

    @staticmethod
    def wait_for_spinner(spinner_in=3, spinner_out=20, locator_spinner=None):
        """
        wait for spinner to be visible, then to be hidden

         spinner_in - timeout in seconds for spinner to be visible,
         spinner_out - timeout in seconds for spinner to be hidden
         locator_spinner - spinner locator
        """
        if locator_spinner is None:
            locator_spinner = "//div[contains(@class,'loader') or contains(@class, 'ajax-overlay-under-popups')]"
            # //div[contains(@class,'parent-overlay')]
        # wait for spinner to be visible
        spinner_located = False
        try:
            logging.info("Wait for spinner to be visible")
            element = WebDriverWait(actions.get_browser(), spinner_in).until(
                expected_conditions.visibility_of_element_located(
                    (By.XPATH, locator_spinner))
            )
            logging.info("Spinner is visible")
            spinner_located = True
        except Exception as e:
            element = None
            logging.info(f"Spinner is not located: {e}")
        if spinner_located:
            # wait for spinner to be hidden
            try:
                element_state = WebDriverWait(actions.get_browser(), spinner_out).until(
                    expected_conditions.staleness_of(element)
                )
                try:
                    WebDriverWait(actions.get_browser(), spinner_out).until_not(
                        expected_conditions.visibility_of_element_located(
                            (By.XPATH, "//div[contains(@class,'parent-overlay')]"))
                    )
                except Exception as e2:
                    logging.info(f"parent-overla is visible {type(e2).__name__}")
            except Exception as e:
                logging.info(e)
                element_state = None
            if element_state:
                logging.info("Spinner is hidden")
            else:
                logging.info("Spinner is still visible")
        else:
            logging.info("Spinner was not displayed")

    @staticmethod
    def wait_for_page_load(timeout=30):
        max_time = int(datetime.now().timestamp()) + timeout
        logging.info(". . . Wait for page loading . . .")
        while max_time > int(datetime.now().timestamp()):
            page_state = actions.get_browser().execute_script('return document.readyState;')
            if page_state == 'complete':
                return
            else:
                actions.wait(1)

    @staticmethod
    @return_on_failure(False)
    def check_if_element_exists(locator, timeout=5):
        try:
            return actions.get_browser().find(locator, timeout=timeout, wait_displayed=timeout).is_displayed()
        except Exception as e:
            logging.info(type(e).__name__)
            return False

    @staticmethod
    def get_current_date(tzone='US/Central'):
        """
        :param tzone: timezone in Yerevan is  'Asia/Yerevan'
        :return: returns time from timezone
        """
        now_utc = datetime.now(timezone('UTC'))
        # Convert to US/Central time zone
        now_time = now_utc.astimezone(timezone(tzone))
        return now_time

    @staticmethod
    def remake_locator(locator, suffix="", new_name=""):
        """
        Add suffix to locator
        """
        by, sel, name = locator
        return by, f"{sel}{suffix}", new_name if new_name else name

    @staticmethod
    def find(locator, timeout=30, should_exist=True, get_text=False, get_attribute=False, wait_displayed=False,
             parent=None):
        new_loc = (locator[0], locator[1])
        try:
            attr = "TEXT" if get_text else str(get_attribute).upper()
            logging.info(f'>> Get "{attr}" from element *{locator[2]}*: {new_loc}' if (get_text or get_attribute)
                         else f'-- Wait for *{locator[2]}*: {new_loc} --')
            browser = actions.get_browser() if not parent else parent
            el = browser.find(new_loc, timeout=timeout, wait_displayed=wait_displayed)
            if get_text:
                logging.info(f"<< {attr} = {el.text}")
                return el.text
            if get_attribute:
                attribute = el.get_attribute(get_attribute)
                logging.info(f"<< {attr} = {attribute}")
                return attribute
            return el
        except Exception as e:
            if should_exist:
                raise ValueError(e)
            else:
                logging.info(f"-->> *{locator[2]}*: {new_loc} Not found")
                return False

    @staticmethod
    def wait_element_and_text(locator, text, timeout=30, retry=5):
        for _ in range(retry):
            el = GeneralHelpers.find(locator, timeout, False, get_text=True)
            if el == text:
                return True
            actions.wait(1)
        return False

    @staticmethod
    def set_attribute(elem, value, attr):
        actions.get_browser().execute_script("arguments[0].setAttribute(arguments[2],arguments[1])", elem, value, attr)

    def get_displayed_element(self, locator, click=False, parent=None, many=False):
        all_data = list()
        for el in self.find_elements(locator=locator, parent=parent):
            if el.is_displayed():
                if click:
                    el.click()
                if many:
                    all_data.append(el)
                else:
                    return el
        return all_data if many else None

    @staticmethod
    def find_and_check_uncheck_checkbox(locator, set_checked, timeout=30, retries=3, should_exist=True):
        while retries:
            retries -= 1
            el = GeneralHelpers.find(locator, timeout=timeout, should_exist=should_exist, wait_displayed=should_exist)
            if not el:
                return False
            try:
                if el.get_attribute("checked"):
                    if not set_checked:
                        el.click()
                else:
                    if set_checked:
                        el.click()
                return el
            except (ElementNotVisibleException, ElementClickInterceptedException) as e:
                logging.info(e)
                # scroll to element
                actions.get_browser().execute_script(scroll_js, el)
            except Exception as e:
                if not retries:
                    raise ValueError(e)
                else:
                    actions.wait(0.3)
                    logging.info(e)

    @staticmethod
    def drop_file(drop_element, file_path: str):
        file_input = actions.get_browser().execute_script(JS_DROP_FILE, drop_element, 0, 0)
        file_input.send_keys(file_path)

    @staticmethod
    def num_generator(size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def find_and_click(locator, timeout=30, should_exist=True, retries=3):
        new_loc = (locator[0], locator[1])
        while retries:
            retries -= 1
            el = GeneralHelpers.find(locator, timeout=timeout, should_exist=should_exist, wait_displayed=should_exist)
            if el or should_exist:
                logging.info(f"-> CLICK on *{locator[2]}*: {new_loc}")
                try:
                    el.click()
                    return el
                except (
                        ElementNotVisibleException, ElementClickInterceptedException,
                        StaleElementReferenceException) as e:
                    logging.info(e)
                    actions.wait(1)
                    # scroll to element
                    try:
                        actions.get_browser().execute_script(scroll_js, el)
                    except:
                        pass
                except Exception as e:
                    if not retries:
                        raise e
                    else:
                        actions.wait(0.3)
                        logging.info(e)
            if not el and not should_exist:
                return False

    @staticmethod
    def scroll_and_click(locator, timeout=30, wait_displayed=True):
        el = GeneralHelpers.find(locator, timeout=timeout, wait_displayed=wait_displayed)
        logging.info(f'-> SCROLL page to element *{locator}*')
        GeneralHelpers.scroll_into_view(locator)
        logging.info(f'-> Click on element *{locator[2]}*')
        GeneralHelpers.find_and_click(locator)
        return el

    @staticmethod
    def wait_and_click(locator, timeout=30, scroll=False, wait_for=None, enabled=False):
        wait_for = wait_for if wait_for else locator
        actions.wait_for_element_present(wait_for, timeout=timeout)
        actions.wait_for_element_displayed(wait_for, timeout=timeout)
        if enabled:
            actions.wait_for_element_enabled(wait_for, timeout=timeout)
        if scroll:
            GeneralHelpers.scroll_into_view(locator)
        actions.click(locator)

    def assert_class_contain(self, el, contain, timeout=10, el_index=0, is_not=False, only_displayed=True):
        class_name = ""
        for i in range(timeout * 10):
            if only_displayed:
                class_name = [i.get_attribute("class") for i in self.find_elements(el) if i.is_displayed()][el_index]
            else:
                class_name = self.find_elements(el, get_attribute="class")[el_index]
            if contain not in class_name if is_not else contain in class_name:
                break
            else:
                time.sleep(.1)
        if is_not:
            assert contain not in class_name, f"Element have in class ({class_name}) value {contain}"
        else:
            assert contain in class_name, f"Element not have in class ({class_name}) value {contain}"

    @staticmethod
    def wait_for_element_clickable(locator: tuple, timeout: int = 30):
        by, loc, desc = locator
        WebDriverWait(actions.get_browser(), timeout).until(
            expected_conditions.element_to_be_clickable((by, loc)))

    @staticmethod
    def wait_for_element_condition(locator, condition, timeout=30, many=False):
        """
        condition - function for check some with element(s)
        for example: lambda el: len(el) > 0
        """
        finder = GeneralHelpers.find_elements if many else GeneralHelpers.find
        for _ in range(timeout):
            elements = finder(locator)
            if condition(elements):
                return True
            actions.wait(1)
        return False

    def prepare_doc_numbers(self):
        data = self.get_data()
        doc_numbers = data.get("doc_numbers", [])
        print(doc_numbers)
        data["doc_numbers"] = [i.split("/")[-1] for i in doc_numbers if i]
        print(data["doc_numbers"])

    @staticmethod
    def find_and_send_keys(locator, send_keys, clear=True, timeout=30, should_exist=True, reset_focus=False):
        el = GeneralHelpers.find(locator, should_exist=should_exist, timeout=timeout, wait_displayed=True)
        if not should_exist and not el:
            return False
        GeneralHelpers.scroll_into_view(locator)
        el.focus()
        el.click()
        if clear:
            logging.info(f'-> CLEAR element *{locator[2]}*')
            el.clear()
        if send_keys is not None:
            logging.info(f'-> FILL in element *{locator[2]}* with: "{send_keys}"')
            el.send_keys(str(send_keys))
        if reset_focus:
            GeneralHelpers.reset_focus()
        return el

    @staticmethod
    def wait_attribute_in_element(locator, value, attr="value", timeout=30):
        el = GeneralHelpers.find(locator, timeout=timeout, wait_displayed=True)
        for _ in range(timeout):
            if el.get_attribute(attr) == value:
                break
            actions.wait(1)
        actions.assert_element_attribute(locator, attr, value)

    @staticmethod
    def find_elements(locator, get_text=False, get_attribute=None, parent=None):
        logging.info(f'-> Find ALL elements *{locator}*')
        new_loc = (locator[0], locator[1])
        browser = actions.get_browser() if not parent else parent
        r = browser.find_all(new_loc)
        if not r:
            # If elements not found - wait and search again
            actions.wait(1)
            r = actions.get_browser().find_all(new_loc)
        if get_text:
            all_text = []
            for el in r:
                try:
                    all_text.append(el.text)
                except StaleElementReferenceException:
                    r.remove(el)
            logging.info(f"<- All *{locator[2]}* text({len(all_text)}): {all_text}")
            return all_text
        if get_attribute:
            all_attr = [i.get_attribute(get_attribute) for i in r]
            logging.info(f"<- All *{locator[2]}* {get_attribute}({len(all_attr)}): {all_attr}")
            return all_attr
        logging.info(f"-- Found *{locator[2]}* elements: ({len(r)}) --")
        return r

    @staticmethod
    def wait_disappear_element(locator, timeout=30):
        logging.info(f"-- Wait till element *{locator}* disappear --")
        WebDriverWait(actions.get_browser(), timeout=timeout). \
            until_not(expected_conditions.presence_of_element_located(locator=(locator[0], locator[1])),
                      message="Element '{}' unexpectedly displayed".format(locator))

    @staticmethod
    def x_translate(text, attribute="text()"):
        return f"translate({attribute},'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{str(text).lower()}'"

    @staticmethod
    def wait_for_elements_count(locator, count: int, retries=5, retry_time=1, strict=False):
        actual_count = None
        for _ in range(retries):
            actual_count = len(actions.get_browser().find_all(locator))
            if actual_count == count:
                return
            else:
                logging.info(f"Waiting count of elements {locator} to be {count}, actual {actual_count}")
                actions.wait(retry_time)
                actual_count = len(actions.get_browser().find_all(locator))
        message = f"Count of elements {locator} is not {count}, but {actual_count}"
        assert not strict, message
        logging.warning(message)

    @staticmethod
    def select_by_text(locator, text, try_count=0):
        from selenium.common.exceptions import NoSuchElementException
        try:
            return actions.select_by_text(locator, text)
        except NoSuchElementException as e:
            if try_count == 3:
                raise e
            actions.wait(0.5)
            return GeneralHelpers.select_by_text(locator, text, try_count + 1)

    @staticmethod
    def kill_proc_by_name(proc_name):
        for process in process_iter():
            if process.name() == proc_name:
                try:
                    username = process.username()
                except AccessDenied:
                    continue
                if os.getlogin() in username:
                    process.terminate()
                    process.wait()


class ClerkSearchGeneralHelpers:
    """
    Clerk Search general purpose helpers
    """

    @staticmethod
    def get_url(ind=0, clerk=True, public_search=False) -> str:
        """
        returns Clerk Search URL for current environment
        clerk=False: returns Public Search URL for current environment
        """
        url = get_url(ind, "search_url")
        return url.format(mode="search" if public_search else "clerksearch", is_clerk=clerk)


class EformHelpers:
    """Eforms general purpose helpers"""

    @staticmethod
    def get_url(ind=0) -> str:
        """
        returns Portal URL for current environment
        """
        return get_url(ind, "portal")


class ErProxyHelpers:
    """
    erProxy general purpose helpers
    """

    @staticmethod
    def get_url() -> str:
        """
        returns erProxy URL for current environment
        """
        env = actions.execution.data.get("env")
        return env.get("erProxy") % (env.get("code"))


class Errors:
    class NoOrderTypeError(Exception):
        ...
