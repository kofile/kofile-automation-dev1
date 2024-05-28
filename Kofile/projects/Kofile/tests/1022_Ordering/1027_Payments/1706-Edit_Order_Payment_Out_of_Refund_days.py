from datetime import date, timedelta
from projects.Kofile.Lib.DB import DB
from projects.Kofile.Lib.test_parent import TestParent
from runner import run_test

description = """
    Go to DB, Payment Method table and update Cash method Is_refundable = 1, Refund_days = 0
    -> Go to CRS as admin
    -> Go to Order Search
    -> Find order out of refund days
    -> Edit order
    -> Check on Edit Order Payment(s) link
    -> Edit Order Payment disable
        """

tags = []


def setup(data):
    with DB(data) as db:
        db.update_refundable_and_refund_days_from_payment_method(refund_days=0)


class test(TestParent):                                                                               # noqa

    def __init__(self, data):
        super(test, self).__init__(data, __name__)

    def __test__(self):
        # initialize dates for search
        from_date = (date.today() - timedelta(weeks=3)).strftime(self.lib.general_helper.DATE_PATTERN)
        to_date = (date.today() - timedelta(days=1)).strftime(self.lib.general_helper.DATE_PATTERN)

        # search order in Order Search by date range (atom tests)
        self.atom.CRS.general.go_to_crs()
        self.lib.CRS.crs.go_to_order_search()
        self.lib.CRS.order_search.search_by_date_range_and_payment_method(from_date, to_date)
        self.lib.CRS.order_search.verify_not_empty_result_or_no_matches_found()
        step = self.lib.CRS.order_search.click_on_order_for_edit_payment()
        assert step, "Not found element for click to edit"
        if step in ("indexing", "capture"):
            self.lib.CRS.order_search.click_pup_in_workflow_btn_yes()
        self.lib.general_helper.wait_for_spinner()
        self.lib.CRS.order_finalization.click_edit_order_payments()
        assert not self.lib.CRS.add_payment.get_payment_method_enabled(), "Field payment method enabled"
        assert self.lib.CRS.add_payment.get_payment_method_transaction_id_enabled(), "Field transaction id disabled"
        assert self.lib.CRS.add_payment.get_payment_method_comment_enabled(), "Field comment disabled"
        assert not self.lib.CRS.add_payment.get_payment_method_amount_enabled(), "Field amount enabled"


if __name__ == '__main__':
    run_test(__file__, env="qa_dallas")
