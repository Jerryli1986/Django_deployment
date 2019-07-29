res=[
 {'index': 'aft-000017_accent_test_20190114', 'docs.count': '8', 'store.size': '130.5kb'},
 {'index': 'aft-000028_test_data_20190426', 'docs.count': '27', 'store.size': '267kb'},
 {'index': 'aft-000022_jerrycsvdecode_20190311', 'docs.count': '2', 'store.size': '37kb'},
 {'index': 'aft-000991_front_20190712', 'docs.count': '28', 'store.size': '183.7kb'},
 {'index': 'aft-000016_dynamic_test_20190107', 'docs.count': '225', 'store.size': '10.1mb'},
 {'index': 'aft-000015_large_files_20190107', 'docs.count': '1', 'store.size': '781.8mb'},
 {'index': 'aft-000014_enron_enhanced_20190704', 'docs.count': '6214', 'store.size': '169.9mb'},
 {'index': 'aft-000995_front_20190712', 'docs.count': '28', 'store.size': '188.1kb'},
 {'index': 'aft-000025_edrm_20190718', 'docs.count': '522', 'store.size': '196.7mb'},
 {'index': 'aft-000993_front_20190712', 'docs.count': '28', 'store.size': '184.2kb'},
 {'index': 'aft-000019_test_20190306', 'docs.count': '27', 'store.size': '126.9kb'},
 {'index': 'aft-000994_front_20190712', 'docs.count': '28', 'store.size': '185.5kb'},
 {'index': 'aft-000015_large_files_20190102', 'docs.count': '1', 'store.size': '66.9mb'},
 {'index': '.triggered_watches', 'docs.count': '0', 'store.size': '538b'},
 {'index': 'aft-000010_unstructured_zip_test_20181217', 'docs.count': '3', 'store.size': '56kb'},
 {'index': 'aft-000018_err_test_20190716', 'docs.count': '7', 'store.size': '653.5kb'},
 {'index': 'aft-000019_test_20190308', 'docs.count': '27', 'store.size': '141.7kb'},
 {'index': '.watches', 'docs.count': '0', 'store.size': '543b'},
 {'index': 'aft-000012_test_20181217', 'docs.count': '27', 'store.size': '124.6kb'},
 {'index': 'aft-000005_panama_paper_csv_20190719', 'docs.count': '213635', 'store.size': '360.2mb'},
 {'index': 'aft-000046_front_un_20190719', 'docs.count': '28', 'store.size': '183.3kb'},
 {'index': 'aft-000002_nips_20180517', 'docs.count': '257', 'store.size': '55mb'},
 {'index': 'aft-000013_test2csv_20181217', 'docs.count': '6', 'store.size': '62.3kb'},
 {'index': 'aft-000992_front_20190712', 'docs.count': '28', 'store.size': '182.9kb'},
 {'index': 'aft-000007_pst_test_20181210', 'docs.count': '1174', 'store.size': '61.2mb'},
 {'index': 'aft-000027_project_data_20190318', 'docs.count': '28', 'store.size': '261.9kb'},
 {'index': 'aft-000003_enron_20190719', 'docs.count': '1016', 'store.size': '52.1mb'},
 {'index': 'aft-000023_jerrycsvdecode_1_20190311', 'docs.count': '100', 'store.size': '366.5kb'},
 {'index': 'aft-000040_test_nist_exclusion_20190705', 'docs.count': '12', 'store.size': '49.5mb'},
 {'index': '.kibana', 'docs.count': '20', 'store.size': '122.9kb'},
 {'index': 'aft-345543_test_20181108', 'docs.count': '47', 'store.size': '224.1kb'},
 {'index': 'aft-000008_techstore_20181211', 'docs.count': '11', 'store.size': '104.7kb'},
 {'index': '.security-6', 'docs.count': '0', 'store.size': '523b'}
 ]
print(([i['index'] for i in res]).index('aft-000028_test_data_20190426'))

in_table={}
for i in res :
    if i['index'] in ['aft-000008_techstore_20181211','.security-6'] :

        in_table.update(i)

print(in_table)
