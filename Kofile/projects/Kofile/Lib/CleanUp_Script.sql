/**

How to execute this script.

1.Declare Tenant 
2.Execute proc with commit, and give @HowToStart parameter 3 - to see result with comments, or 2 - to see result without comments

How to test this script
Execute proc with Rollback,  @HowToStart=6 ( debug mode)
After execute proc copy result (result.png) and past in other query page, with begin transaction and rollback
Execute query
Before rollback and after you can select any data to check result before and after script execution
For more details see comment under task https://kofile.tpondemand.com/RestUI/Board.aspx#page=board/5126489022850675744&appConfig=eyJhY2lkIjoiQzJCREZCODRBMDUyMjJBQTc5QjQ2NTM0QTRGMTVCNzUiLCJhcHBDb250ZXh0Ijp7InByb2plY3RDb250ZXh0Ijp7Im5vIjpmYWxzZX0sInRlYW1Db250ZXh0Ijp7Im5vIjp0cnVlfX19&searchPopup=task/82967

**/

DECLARE @TENANT_TO_WORK sysname = 'VG48000'

SET NOCOUNT ON
DECLARE @par [dbo].[tTruncateList]
INSERT INTO @par (   TableSchemaName
                   , TableToTruncate
                   , wherePredicates
                 )
SELECT  t.TableSchemaName
      , t.TableToTruncate
      , t.wherePredicates
FROM ( VALUES

--(@TENANT_TO_WORK, 'ACCOUNT_ACTIVITY', NULL),
--(@TENANT_TO_WORK, 'ACCT_USERID_SUBSCRIPTION_PLAN', NULL),
--(@TENANT_TO_WORK, 'BM_BALANCEDETAIL', NULL),
--(@TENANT_TO_WORK, 'BM_BALANCEPOST', NULL),
--(@TENANT_TO_WORK, 'BM_BALANCESESSION', NULL),
--(@TENANT_TO_WORK, 'CRS_LOCKED_ELEMENT', NULL),
--(@TENANT_TO_WORK, 'DEVICE_JOB', 'WHERE DEVICE_JOB_RECURRING_TYPE=2'),
--(@TENANT_TO_WORK, 'ER_PACKAGE', NULL),
--(@TENANT_TO_WORK, 'ER_PACKAGE_HISTORY', NULL),
--(@TENANT_TO_WORK, 'KOFAX_CAPTURE', NULL),
--(@TENANT_TO_WORK, 'KOFILE_INDEX', NULL),
--(@TENANT_TO_WORK, 'KOFILE_INDEX_HISTORY', NULL),
(@TENANT_TO_WORK, 'ORDER', 'WHERE (order_id not in (select order_id from [<schemaname>].[ORDER] where (Aduser_id  in (117,151,155,156,171) OR ADUSER_ID IS NULL ) and ORDER_DATE BETWEEN DATEADD(day,-7, GETDATE()) AND DATEADD(day,-6, GETDATE())))'),
(@TENANT_TO_WORK, 'ORDER_AUDIT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'ORDER_ER', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'ORDER_EVENT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'ORDER_EXPORT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'ORDER_FEE_FUND', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'ORDER_HISTORY', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_APPLICANT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_ASYNC_PROCESS', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_ATTACHMENT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_AUDIT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_DETAILS', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_DISCOUNT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_FEE_CRITERIA', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_FEE_CRITERIA_AUDIT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_FEE_FUND', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_FEE_FUND_AUDIT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_HISTORY', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.[ORDER_ITEM _ID])'),
(@TENANT_TO_WORK, 'ORDER_ITEM_MISSING_CONTENT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_NOTE', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_PARTY', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_ITEM_STATUS', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.ORDER_ITEM_ID)'),
(@TENANT_TO_WORK, 'ORDER_PAYMENT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'ORDER_PAYMENT_AUDIT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'BM_BALANCE', 'WHERE (TBL.Aduser_id not in (117,151,155,156,171))'),
(@TENANT_TO_WORK, 'CAPTURING_TASK', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'INDEXING_TASK', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'SHOPPINGCART_ITEMS', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.DM_ID=TBL.DM_ID)'),
(@TENANT_TO_WORK, 'VERIFICATION_TASK',  'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'VERIFICATION_QUEUE', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER] T WHERE T.ORDER_ID=TBL.ORDER_ID)'),
(@TENANT_TO_WORK, 'DOC_MASTER', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.DM_ID=TBL.DM_ID)'),
(@TENANT_TO_WORK, 'DM_CONTENT', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[DOC_MASTER] T WHERE T.DM_ID=TBL.DM_ID)'),
(@TENANT_TO_WORK, 'DM_CONTENT_VERSION', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[DOC_MASTER] T WHERE T.DM_ID=TBL.DM_ID)'),
(@TENANT_TO_WORK, 'DM_DMREF', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[DOC_MASTER] T WHERE T.DM_ID=TBL.DM_ID)')
--(@TENANT_TO_WORK, 'VERIFICATION_TASK_ORDER_ITEM', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.[ORDER_ITEM _ID])'),
--(@TENANT_TO_WORK, 'INDEXING_TASK_ORDER_ITEM', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.[ORDER_ITEM _ID])'),
-- (@TENANT_TO_WORK, 'CAPTURING_TASK_ORDER_ITEM', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.ORDER_ITEM_ID=TBL.[ORDER_ITEM _ID])'),
--(@TENANT_TO_WORK, 'SHOPPINGCART', NULL),

--(@TENANT_TO_WORK, 'ORDER_SYS_LOCK', NULL),
--(@TENANT_TO_WORK, 'ORDER_TAGS', NULL),
--(@TENANT_TO_WORK, 'SCANNED_FILE', NULL),
--(@TENANT_TO_WORK, 'SCANNER_BATCH', NULL),
--(@TENANT_TO_WORK, 'SCANNER_BATCH_HISTORY', NULL),
--(@TENANT_TO_WORK, 'SCANNER_TASK', NULL),
--(@TENANT_TO_WORK, 'SEARCH_HISTORY', NULL),
--(@TENANT_TO_WORK, 'SEARCH_ORDER', NULL),
--(@TENANT_TO_WORK, 'SEARCH_ORDER_ITEM', NULL),
--(@TENANT_TO_WORK, 'SESSION', NULL),
-- (@TENANT_TO_WORK, 'BM_BALANCE_CHEQUE', 'WHERE EXISTS(SELECT 1 FROM [<schemaname>].[ORDER_ITEM] T WHERE T.DM_ID=TBL.DM_ID)'),
--(@TENANT_TO_WORK, 'SHOPPINGCART_ITEM_ADDRESS', NULL),
--(@TENANT_TO_WORK, 'SHOPPINGCART_PAYMENTDETAILS', NULL),
--(@TENANT_TO_WORK, 'TEMP_CARTEXPORT_ORDER', NULL),
--(@TENANT_TO_WORK, 'USER_KDRIVE', NULL),


--(@TENANT_TO_WORK, 'WORKFLOW_CONTENT', NULL)

)
t ( TableSchemaName, TableToTruncate, wherePredicates ) 

--------------------------
-- @HowToStart: @Debug,@Recycle,@Verbose -> 7 == set all, 5 == @Debug && @Verbose, 3 == @Recycle,@Verbose etc
BEGIN TRAN

EXEC dbo.sp_truncate_tbl_with_ref_fk @par, @HowToStart = 6 --2

ROLLBACK -- Comment this line after testing
--COMMIT -- Uncomment this line after testing