"""
Provides work(download, compare, remove, etc) with files
"""
import os
import re
from datetime import datetime
import PyPDF2
# from pypdf import PdfReader
import fitz
import requests
from PIL import Image

from projects.Kofile.Lib.test_parent import LibParent
from projects.Kofile.Lib.DB import DataBaseWithVPN
from projects.Kofile.Lib.Azure import AzureBlobStorage

CHECK_CONTENT = False


class Files(LibParent):
	def __init__(self):
		super(Files, self).__init__()

	@staticmethod
	def compare_print_pdf_files_format_new(file, expected_data, equals_pages=None):
		pdf = PyPDF2.PdfReader(file)
		if equals_pages:
			assert len(pdf.pages) == equals_pages, f"PDF files don't have the same number of pages. Expected: " \
												   f"{equals_pages}, actual: {len(pdf.pages)}"
			return
		assert len(pdf.pages) == expected_data["pages"], f"PDF files don't have the same number of pages. Expected: " \
														 f"{expected_data['pages']}, actual: {len(pdf.pages)}"
		for number, page in enumerate(pdf.pages):
			lines = [i.strip() for i in page.extract_text().split("\n") if
					 i.strip() and not repr(i.strip()).lstrip('"\'').startswith("\\x")]
			for a, line in enumerate(expected_data["content"][number]):
				if line:
					assert line == lines[a], f"PDF expected row '{lines[a]}' is not equal '{line}' in file.\n" \
											 f"Expected content: {expected_data['content'][number]}\n" \
											 f"Actual content:   {lines}\n" \
											 f"Page: {number}"
		file.close()

	@staticmethod
	def compare_txt_files_new(data, expected_data):
		for line in expected_data["content"]:
			if line:
				assert line in data, f"TXT expected row '{line}' not found in file.\n" \
									 f"Expected content: {expected_data['content']}\n" \
									 f"Actual content:   {data}"

	def compare_print_pdf_files_format(self, file1, file2, exception_list, val=None):
		with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
			f1_read = PyPDF2.PdfReader(f1)
			f1_rows = f1_read.getPage(0)
			f2_read = PyPDF2.PdfReader(f2)
			f2_rows = f2_read.getPage(0)
			if len(f1_read.pages) != len(f2_read.pages):
				self._actions.error("PDF files don't have the same number of pages")
			lst1 = [elem.strip() for elem in f1_rows.extract_text().split("\n") if
					elem.strip() or not repr(elem).startswith("'\\x")]
			lst2 = [elem.strip() for elem in f2_rows.extract_text().split("\n") if
					elem.strip() or not repr(elem).startswith("'\\x")]
			for l1, l2 in zip(lst1, lst2):
				for fmt in ('%I:%M %p', '%B %d', '%B %d, %Y', '%B %d, %Y %I:%M %p', '%B', '%I:%M%p',
							'%m/%d/%Y %I:%M %p', '%m/%d/%Y'):
					try:
						datetime.strptime(l1, fmt)
						parse_str = False
						break
					except ValueError:
						parse_str = l1
				if parse_str and l1 != l2:
					if any(ex in l1 for ex in exception_list) or "Name_" in l1 or "NAME_" in l1 \
							or re.match('\\d+ - \\d+', l1, flags=0):
						continue
					if val and val in l1:
						self._actions.error(f"Amount value is incorrect")
						continue
					self._actions.error(f"PDF row '{l1}' in file '{file1}' is not equal '{l2}' in file {file2}")
		f1.close()
		f2.close()

	def compare_txt_files(self, file1, file2, exception_list):
		with open(file1, 'r', encoding="utf8") as f1, open(file2, 'r', encoding="utf8") as f2:
			doc_1, doc_2 = [i for i in f1.readlines() if i.strip()], [i for i in f2.readlines() if i.strip()]
			for l1, l2 in zip(doc_1, doc_2):
				if l1.strip() != l2.strip():
					if any(ex in l1 for ex in exception_list) or "Book:" in l1 or "Date/Time:" in l1:
						continue
					self._actions.error(f"The row '{l1}' is not equal '{l2}'")
		f1.close()
		f2.close()

	@staticmethod
	def get_pdf_files_content(pdf_file):
		with open(pdf_file, 'rb') as file:
			file_read = PyPDF2.PdfReader(file)
			file_first_page = file_read.getPage(0)
			# file_content = file_first_page.extractText()
			file_content = file_first_page.extract_text()
		file.close()
		return file_content

	@staticmethod
	def pdf_to_images(pdf_bytes):
		result = dict()
		doc = fitz.open(stream=pdf_bytes, filetype="pdf")
		for page in doc.pages():
			pix = page.get_pixmap()
			img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
			result[page.number + 1] = img
		return result

	def remove_file(self, file):
		if os.path.exists(file):
			os.remove(file)
		else:
			self._actions.step(f"The file {file} does not exist")

	def compare_strings(self, s1, s2):
		if s1 == s2:
			self._actions.step(f"The strings are equal")
		else:
			self._actions.error(f"The string '{s1}' is not equal '{s2}'")

	@staticmethod
	def get_barcode(data, doc_num, doc_type, year):
		return f"*VG-{DataBaseWithVPN(data).get_doc_type_id_by_doc_type_code(doc_type)}-{year}-{doc_num}*"

	def open_yopmail_in_new_tab_and_download_pdf(self, email, download_dir):
		link = "https://yopmail.com/"
		self._actions.get_browser().execute_script("window.open('{}');".format(link))
		self._actions.switch_to_window_by_index(1)
		self._general_helper.find_and_send_keys(self._pages.mail.login_input_xpath, email)
		self._general_helper.scroll_and_click(self._pages.mail.login_btn_xpath)
		self._actions.wait(2)
		self._actions.switch_to_frame('ifinbox')
		self._general_helper.scroll_and_click(self._pages.mail.email_row_xpath)
		self._actions.switch_to_parent_frame()
		self._actions.switch_to_frame('ifmail')

		cookies_copy = {}
		for driver_cookie in self._actions.get_cookies():
			cookies_copy[driver_cookie["name"]] = driver_cookie["value"]
		request = requests.get(self._actions.get_element_attribute(self._pages.mail.attached_pdf_xpath, 'href'),
							   cookies=cookies_copy)
		file_name = os.path.join(download_dir,
								 str(self._actions.get_element_text(self._pages.mail.attached_pdf_name_xpath)).strip())
		with open(file_name, 'wb') as file:
			file.write(request.content)
		return file_name

	def clear_download_folder(self, download_dir, wait_for_file=True):
		for _ in range(10):
			address, dirs, files = next(os.walk(download_dir))
			if files:
				file_count = len(files)
				for f in files:
					os.remove(os.path.join(address, f))
				return file_count
			if not wait_for_file:
				return 0
			self._actions.wait(3)
		return 0

	def get_last_downloaded_file(self, download_dir):
		for _ in range(10):
			address, dirs, files = next(os.walk(download_dir))
			self._logging.info(f"Files found: {files}")
			if files:
				for i in files:
					if ".tmp" not in i:
						return os.path.join(address, i)
			self._actions.wait(3)
		return None

	def download_and_compare_pdf_new(self, data, expected_data_name, folder_pattern="wfcontent-{}-printfolder",
									 equals_pages=None, filename=None, device_job_id=None, row=0):
		azure = AzureBlobStorage(data)
		if expected_data_name and not equals_pages:
			expected_data = self.get_expected_data(data, expected_data_name)
		else:
			expected_data = None
		container = folder_pattern.format(data['env']['code'])
		if isinstance(filename, str):
			file_name = DataBaseWithVPN(data).get_file_name_by_started_pattern_from_xml(
				filename, device_job_id=device_job_id)
		else:
			file_name = filename[0] if filename else DataBaseWithVPN(data).get_file_name_from_xml(
				row, device_job_id=device_job_id)
		assert file_name, f"Cant find file with name {filename} in db"
		if CHECK_CONTENT:
			downloaded_file = azure.download_file(file_name.replace("\\", "/"), container)
			self.compare_print_pdf_files_format_new(downloaded_file, expected_data, equals_pages)
		else:
			azure.check_blob_existence_in_container(file_name.replace("\\", "/"), container)

	def download_and_compare_pdf(self, data, file, exception_list, row=0, val=None, device_job_id=None,
								 folder_pattern="wfcontent-{}-printfolder", equals_pages=None, file2=None,
								 filename=None):
		db = DataBaseWithVPN(data)
		azure = AzureBlobStorage(data)
		container = folder_pattern.format(data['env']['code'])
		if file2:
			file_name = db.get_file_name_by_started_pattern_from_xml(file, device_job_id=device_job_id)
			file = file2
		else:
			if filename:
				file_name = db.get_file_name_by_started_pattern_from_xml(filename, device_job_id=device_job_id)
			else:
				file_name = db.get_file_name_from_xml(row, device_job_id=device_job_id)
		assert file_name, f"Cant find filename in db"
		if CHECK_CONTENT:
			azure.download_all_blobs_in_container(container, file_name.replace("\\", "/"), self._names.print_files)
			file_in_folder = os.path.join(self._names.print_files, file_name)
			file_r = file.replace("XXXXX_", f"{data.env.get('config_name')}_")
			if equals_pages:
				with open(file_in_folder, "rb") as f:
					reader = PyPDF2.PdfReader(f)
					assert equals_pages == len(reader.pages), \
						f"PDF have {len(reader.pages)} pages, but must have {equals_pages}"
			else:
				self.compare_print_pdf_files_format(file_in_folder, file_r, exception_list, val)
			self.remove_file(file_in_folder)
		else:
			azure.check_blob_existence_in_container(file_name.replace("\\", "/"), container)

	def download_and_compare_txt(self, data, file1, file2, exception_list):
		db = DataBaseWithVPN(data)
		azure = AzureBlobStorage(data)
		container = f"wfcontent-{data['env']['code']}-printfolder"
		file_name = db.get_file_name_by_started_pattern_from_xml(file1)
		assert file_name, f"Cant find filename in db with {file1}"
		if CHECK_CONTENT:
			azure.download_all_blobs_in_container(container, file_name, self._names.print_files)
			file_in_folder = os.path.join(self._names.print_files, file_name)
			file_r = file2.replace("XXXXX_", f"{data.env.get('config_name')}_")
			self.compare_txt_files(file_in_folder, file_r, exception_list)
			self.remove_file(file_in_folder)
		else:
			azure.check_blob_existence_in_container(file_name, container)

	def get_last_printing_file_from_db(self):
		db = DataBaseWithVPN(self._actions.get_data())
		data = db.get_file_name_by_started_pattern_from_xml(self._names.printing_pattern)
		assert data, f"Cant find any filename in db"
		return data

	def download_and_compare_txt_new(self, data, expected_data_name, filename):
		azure = AzureBlobStorage(data)
		container = f"wfcontent-{data['env']['code']}-printfolder"
		expected_data = self.get_expected_data(data, expected_data_name)
		if isinstance(filename, str):
			file_name = DataBaseWithVPN(data).get_file_name_by_started_pattern_from_xml(filename)
		else:
			file_name = filename[0] if filename else DataBaseWithVPN(data).get_file_name_from_xml()
		assert file_name, f"Cant find filename in db with {filename}"
		if CHECK_CONTENT:
			downloaded_file = azure.get_text_from_file(file_name.replace("\\", "/"), container)
			self.compare_txt_files_new(downloaded_file, expected_data)
		else:
			azure.check_blob_existence_in_container(file_name.replace("\\", "/"), container)

	def get_expected_data(self, data, expected_data_name):
		expected_class = getattr(self._names.printing_data, data.env.get('name')) if hasattr(
			self._names.printing_data, data.env.get('name')) else None
		expected_class_2 = getattr(self._names.printing_data, data.env.get('config_name')) if hasattr(
			self._names.printing_data, data.env.get('config_name')) else None
		assert expected_class or expected_class_2, f"class PrintData in file printing_data.py not have class " \
												   f"with name {data.env.get('name')} or {data.env.get('config_name')}"
		expected_data = getattr(expected_class, expected_data_name) if hasattr(
			expected_class, expected_data_name) else None
		if not expected_data:
			expected_data = getattr(expected_class_2, expected_data_name) if hasattr(
				expected_class_2, expected_data_name) else None
		assert expected_data, f"class {expected_class.__name__} in class PrintData in file printing_data.py " \
							  f"not have variable  with name {expected_data_name}"
		self._actions.step(f"using printing data:\nclass: {expected_class.__name__}\nvariable: {expected_data_name}")
		return self.prepare_expected_data(expected_data)

	def prepare_expected_data(self, expected_data):
		if not self._data.get('order_number'): return expected_data
		db = DataBaseWithVPN(self._data)
		if self._data.doc_sequence_number and self._data.doc_sequence_number > 0:
			doc_index = self._data.doc_sequence_number - 1
		else:
			doc_index = 0
		order_data = db.get_order_total_datetime_num_oit_price()[doc_index]
		keys = ['order_total', 'order_date', 'order_time', 'order_num', 'order_item_price']
		order_data = dict(zip(keys, order_data))
		if 'pages' in expected_data:
			order_data['order_time'] = order_data['order_time'].replace(' ', '')
			for key in keys:
				expected_data['content'][0] = list(
					map(lambda x: order_data.get(key) if x == f'%{key}' else x, expected_data['content'][0]))
		else:
			for key in keys:
				if key != 'order_num': expected_data['content'].append(order_data.get(key))
		return expected_data
