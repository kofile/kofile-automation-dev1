from golem import actions
from projects.Kofile.api.api_services import ApiService


class CaptureAPI(ApiService):

    def get_available_doc_types(self, doc_group=None, term="a"):
        data = actions.execution.data
        doc_group = doc_group if doc_group else data.config.test_data(f"{data.OIT}.doc_group")
        url = f"{self.domain}/Capture/GetDocumentType?term={term}&docGroupDesc={doc_group.replace(' ', '%20')}"
        r = self.request_("GET", url).json()
        return r

    def get_doc_type(self, doc_group=None, term="a"):
        all_doc_types = self.get_available_doc_types(doc_group=doc_group, term=term)
        assert all_doc_types, "Document Type(s) no found!"
        return all_doc_types[0]['Value']
