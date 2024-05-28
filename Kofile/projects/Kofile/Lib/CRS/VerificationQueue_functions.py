from projects.Kofile.Lib.test_parent import LibParent


class VerificationQueue(LibParent):
    def __init__(self):
        super(VerificationQueue, self).__init__()

    def verify_order_status(self, status):
        """Verify status of order in verification queue"""
        data = self._general_helper.get_data()
        self._actions.verify_element_text(self._pages.CRS.general.status_by_order_number(data["order_number"]),
                                          data['config'].get_status(f'Verification.{status}.value'))
