from golem import actions
from projects.Kofile.api.api_services import ApiService


class FrontOfficeAPI(ApiService):

    def company_accounts_search(self, account_code="", account_name=""):
        actions.step(f"-> API -> Search company accounts: *{account_code} {account_name}*")
        url = f"{self.domain}/Company/GetCompanyAccountsSearchResult" \
              f"?accountName={account_name}&accountCode={account_code}"
        r = self.request_("GET", url).json()
        return r

    def get_company_account_info_by_id(self, account_id):
        actions.step(f"-> API -> Get company account ID({account_id}) info")
        url = f"{self.domain}/Company/EditCompanyAccount?accountId={account_id}"
        r = self.request_("GET", url).json()
        return r

    def get_company_account_info(self, account_code="", account_name=""):
        if not account_code and not account_name:
            raise ValueError("Account code and/or company name not provided!")
        account_id = None
        response = self.company_accounts_search(account_code, account_name)
        for i in response:
            if i["AccountCode"] == account_code or i["AccountName"] == account_name:
                account_id = i["Id"]
                break
            else:
                raise ValueError(f"Company[{account_code}, {account_name}] not found in: {response}")
        r = self.get_company_account_info_by_id(account_id)
        return r
