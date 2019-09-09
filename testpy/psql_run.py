import elasticsearch
import subprocess
from collections import OrderedDict
from services.connection_services import sql_connectors, file_connectors

class FileCountCheck():
    """
    Runs a QC on the number of documents in the index compared to the initial number sent into the ingest pipeline
    by analysing the ingest logs
    Takes the barcode of the index, the index, the SQL connection to the log database and the host address
    of the elasticsearch cluster
    Outputs to /var/www/dust/dustpan/load/static/QC/
    """
    def __init__(self, barcode, index, sql_conn, host, system_type, db_flavour):
        self.barcode = barcode
        self.index = index
        self.conn = sql_conn
        self.es = host
        self.system_type = system_type
        self.db_flavour = db_flavour
        # Records the file paths of missed files is present
        self.failed_pp = None
        self.failed_misc = None

    def _check_logging_completed(self):
        """
        Retrieves the last entry in the log.master table for barcode specified and returns true if it records
        the creation of the index.
        """
        sql_cmd = '''
                    SELECT comments
                    FROM log.master 
                    WHERE ingest_id = '{}' 
                    ORDER BY datetime DESC 
                    LIMIT 1; 
                  '''.format(self.barcode)
        comment = self.conn.select(sql_cmd).fetchall()
        if comment:
            return comment[0][0].startswith('SUCCESS: Index ' + self.index + ' created')
        else:
            return False

    def _get_initial_count(self):
        """
        Runs shell command on server to find the number of files in the initial folder corresponding to the barcode
        """
        command = 'find /data/SAMPLE/{}/ -type f | wc -l'.format(self.barcode)
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        total = int(process.stdout)
        return total

    def _get_count_index(self):
        """
        Returns the number of documents in the index
        """
        self.es.indices.refresh(index=self.index)
        index_count = self.es.count(self.index).get('count')
        return index_count

    def _get_count_deduped(self):
        """
        Returns the number of files which were not indexed because they were duplicate documents and had the same md5
        """
        sql_cmd = '''
                    SELECT COUNT(md5) -COUNT(DISTINCT md5)
                    FROM meta.loose_file lf
                    JOIN source.system_part sp 
                        ON lf.system_id = sp.system_id
                    WHERE sp.aft_barcode = '{}';
                  '''.format(self.barcode)
        count = self.conn.select(sql_cmd).fetchall()
        return int(count[0][0])

    def _get_count_failed_password_protected(self):
        """
        Returns the number of documents which failed to index due to being password protected or unsupported
        """
        sql_cmd = '''
                    SELECT file_path
                    FROM log.master
                    WHERE ingest_id = '{}'
                        AND action_type = 'index'
                        AND comments LIKE 'FAIL:%PasswordProtected%';   
                    '''.format(self.barcode)
        res = self.conn.select(sql_cmd).fetchall()
        self.failed_pp = res
        return len(res)

    def _get_count_failed_misc(self):
        """
        Returns the number of documents which failed to index that were not password protected or unsupported
        """
        sql_cmd = '''
                    SELECT file_path, comments
                    FROM log.master
                    WHERE ingest_id = '{}'
                        AND action_type = 'index'
                        AND comments LIKE 'FAIL:%'
                        AND comments NOT LIKE '%PasswordProtected%';
                  '''.format(self.barcode)
        res = self.conn.select(sql_cmd).fetchall()
        self.failed_misc = res
        return len(res)

    def _get_count_archives(self):
        """
        Returns the number of archive folders which have been inflated
        """
        sql_cmd = '''
                    SELECT COUNT(*)
                    FROM log.master
                    WHERE ingest_id = '{}'
                        AND action_type = 'inflate';
                  '''.format(self.barcode)
        count = self.conn.select(sql_cmd).fetchall()
        return int(count[0][0])

    def _get_count_inflated(self):
        """
        Number of documents which have been inflated from archive folders
        """
        sql_cmd = '''
                    SELECT COUNT(*)
                    FROM meta.loose_file lf
                        JOIN source.system_part sp 
                        ON lf.system_id = sp.system_id
                    WHERE source_archive IS NOT NULL
                        AND sp.aft_barcode = '{}';
                  '''.format(self.barcode)
        count = self.conn.select(sql_cmd).fetchall()
        return int(count[0][0])

    def _get_count_nist_filtered(self):
        """
        Number of documents which have been filtered by meta.blacklist_file_type
        """
        sql_cmd = '''
                    SELECT
                           count(*)
                        FROM meta.loose_file f
                        INNER JOIN source.system_part s
                            ON f.system_id = s.system_id
                        LEFT OUTER JOIN meta.process_method p
                            ON f.file_type = p.file_type
                        LEFT OUTER JOIN meta.nist_list n
                            ON upper(f.md5) = n.md5
                        WHERE (p.process = 'ingest' OR p.process IS NULL)
                        AND s.aft_barcode = '{}'
                        AND f.for_processing = TRUE
                        AND n.md5 IS NOT NULL
                  '''.format(self.barcode)
        count = self.conn.select(sql_cmd).fetchall()
        return int(count[0][0])

    def _get_count_type_filtered(self):
        """
        Number of documents which have been filtered by meta.blacklist_file_type
        """
        sql_cmd = '''
                    SELECT
                           count(*)
                        FROM meta.loose_file f
                        INNER JOIN source.system_part s
                            ON f.system_id = s.system_id
                        LEFT OUTER JOIN meta.process_method p
                            ON f.file_type = p.file_type
                        LEFT OUTER JOIN meta.nist_list n
                            ON upper(f.md5) = n.md5
                        LEFT OUTER JOIN meta.blacklist_file_type bl 
                            ON f.file_type = bl.file_type AND bl.removed_from_list = FALSE
                        WHERE (p.process = 'ingest' OR p.process IS NULL)
                        AND s.aft_barcode = '{}'
                        AND f.for_processing = TRUE
                        AND n.md5 IS NULL
                        AND bl.file_type IS NOT NULL
                  '''.format(self.barcode)
        count = self.conn.select(sql_cmd).fetchall()
        return int(count[0][0])

    def _get_row_counts_structured(self):
        '''
           Number of total rows for all tables
        '''
        sql_cmd = '''
                       SELECT sum(row_count) 
                       FROM meta.table_meta as TM
                       INNER JOIN meta.database_meta as DM
                               ON TM.system_id = DM.system_id
                       INNER JOIN source.system_part as SP
                               ON DM.system_id = SP.system_id
                       where  SP.aft_barcode = '{}'; 
                  '''.format(self.barcode)
        count = self.conn.select(sql_cmd).fetchall()
        count_rows = int(count[0][0])
        if self.db_flavour == 'CSVConnector':
            count_rows = count_rows + self._get_table_number()
        return count_rows

    def _get_table_number(self):
        '''
           Number of total rows for all tables
        '''
        sql_cmd = '''
                          SELECT count(row_count) 
                          FROM meta.table_meta as TM
                          INNER JOIN meta.database_meta as DM
                                  ON TM.system_id = DM.system_id
                          INNER JOIN source.system_part as SP
                                  ON DM.system_id = SP.system_id
                          where  SP.aft_barcode = '{}'; 
                     '''.format(self.barcode)
        count = self.conn.select(sql_cmd).fetchall()
        return int(count[0][0])

    def _write(self, counts, outcome):
        """
        Write the counts to a text file contained in the load/static/QC file and writes the file paths of those
        which failed to index
        counts: Dictionary of the counts from the QC
        outcome: String stating if counts matched
        """
        file_name = self.index + '_QC.txt'
        report_path = '/var/www/dust/dustpan/load/static/QC/{}'.format(file_name)
        with open(report_path, 'w', newline='') as txtfile:
            for name, count in counts.items():
                txtfile.write(name + ': ' + str(count) + '\n')
            txtfile.write('Validated if: ')
            if self.system_type == 'fs':
                txtfile.write(
                    'Index Count = Initial Count + Expanded Count - Deduped Count - Archive Count - Failed Count - Filtered Count')
                txtfile.write('\n' + outcome + '\n')
                # Writes file paths which  failed to index because they were password protected or unsupported
                if self.failed_pp:
                    txtfile.write('\nPassword Protected or Unsupported Files: \n')
                    for file in self.failed_pp:
                        txtfile.write(file[0] + '\n')
                # Writes file paths and the corresponding error that caused failure
                if self.failed_misc:
                    txtfile.write('\nMiscellaneous Failed Files: \n')
                    for file in self.failed_misc:
                        txtfile.write(file[0] + '\n')
                        txtfile.write('Error: ' + file[1] + '\n')
            elif self.system_type == 'db':
                txtfile.write('Index Count = Initial Count ')
                txtfile.write('\n' + outcome + '\n')
        return report_path

    def get_all_counts(self):
        """
        Get the index and initial counts and the failed, deduped, archive and expanded counts
        Print the counts
        """
        counts = OrderedDict()
        if self.system_type == 'fs':
            counts = OrderedDict([('Index Count', self._get_count_index()),
                                  ('Initial Count', self._get_initial_count()),
                                  ('Deduped Count', self._get_count_deduped()),
                                  ('Failed (Password Protected, Empty or Incompatible)',
                                   self._get_count_failed_password_protected()),
                                  ('Miscellaneous Failed', self._get_count_failed_misc()),
                                  ('Archive Count', self._get_count_archives()),
                                  ('Expanded Count', self._get_count_inflated()),
                                  ('Filtered Count', self._get_count_nist_filtered() + self._get_count_type_filtered())])
        elif self.system_type == 'db':
            counts = OrderedDict([('Index Count', self._get_count_index()),
                                  ('Initial Count', self._get_row_counts_structured()),
                                  ('Deduped Count', 0),
                                  ('Failed (Password Protected, Empty or Incompatible)',0),
                                  ('Miscellaneous Failed', 0),
                                  ('Archive Count', 0),
                                  ('Expanded Count', 0),
                                  ('Filtered Count', 0)])

        for name, count in counts.items():
            print(name + ' ' + str(count))
        return counts

    def validate_count(self):
        """
        Validate the index count compared to the initial count by accounting for missing files and those which have
        been expanded.
        """
        # Check logging completed
        if self._check_logging_completed():
            counts = self.get_all_counts()

            print('Verifying: ')
            if self.system_type == 'fs':
                print('Index Count = Initial Count + Expanded Count - Deduped Count - Archive Count - Failed Count - Filtered Count')
                # Check if counts add up correctly
                if counts['Index Count'] == counts['Initial Count'] + counts['Expanded Count'] - counts['Deduped Count'] \
                        - counts['Archive Count'] - counts['Failed (Password Protected, Empty or Incompatible)'] \
                        - counts['Miscellaneous Failed'] - counts['Filtered Count']:
                    print('Counts Matched')
                    # fpath = self._write(counts, 'Counts Matched')
                    return True #, fpath
                else:
                    print('Counts did not match')
                    # fpath = self._write(counts, 'Counts did not Match')
                    return False #, fpath
            else:
                # Validate the index count compared to the initial count by accounting for sum of row number of all tables
                print('Index Count = Initial Count ')
                # Check if counts add up correctly

                if counts['Index Count'] == counts['Initial Count']:
                    print('Counts Matched')
                    # fpath = self._write(counts, 'Counts Matched')
                    return True #, fpath
                else:
                    print('Counts did not match')
                    # fpath = self._write(counts, 'Counts did not Match')
                    return False #, fpath
        else:
            print('Logging incomplete. Unable to complete QC!')
            return False

    def get_ingest_time(self):
        sql_cmd = ''' SELECT round(EXTRACT(EPOCH FROM (max(datetime)-min(datetime)))) 
                      from log.master 
                      where ingest_id =  '{}'; 
                  '''.format(self.barcode)
        ingest_time_select = self.conn.select(sql_cmd).fetchall()
        return int(ingest_time_select[0][0])

    def get_index_size(self):
        index_info = self.es.cat.indices(index=self.index, h=['pri.store.size'], format='json')
        return index_info[0]['pri.store.size']

    def get_barcode_list(self):
        sql_cmd = '''
                    select substring(index_alias,1,position(' ' in index_alias)) from request.elastic_index;
                  '''
        barcode_select = self.conn.select(sql_cmd)
        heads = [col.name for col in self.conn.cursor.description]
        barcodes = tuple(dict(zip(heads, ind)) for ind in barcode_select)
        return barcodes

    def get_index_name(self):
        sql_cmd = '''
                    SELECT index_name
                    FROM request.elastic_index  els
                    WHERE els.index_alias like '{}%';
                  '''.format(self.barcode)
        index_name_select = self.conn.select(sql_cmd).fetchall()
        return int(index_name_select[0][0])

    def get_system_type(self):
        sql_cmd = '''
                    SELECT lower(system_type)
                    FROM source.system_part  SP
                    WHERE SP.aft_barcode = '{}'; 
                  '''.format(self.barcode)
        system_type_select = self.conn.select(sql_cmd).fetchall()
        return int(system_type_select[0][0])

    def get_db_flavour(self):
        if self.system_type == 'fs':
           return None
        else:
            sql_cmd = '''
                    SELECT db_flavour
                    FROM meta.database_meta DM
                    INNER JOIN source.system_part as SP
                                  ON DM.system_id = SP.system_id
                    WHERE SP.aft_barcode = '{}'; 
                  '''.format(self.barcode)
            db_flavour_select = self.conn.select(sql_cmd).fetchall()
            return db_flavour_select[0][0]

    def clear_table(self):
        sql_cmd = '''
           DELETE
           FROM
           request.QC_table;
          '''
        self.conn.delete(sql_cmd)

    def save_qc_table(self,counts,validate,ingest_time,index_size):
        q = ''' 
               INSERT INTO request.QC_table 
               ( barcode,
                 index_name,
                 Index_Count,
                 Initial_Count,
                 Deduped_Count,
                 Failed_(Password Protected_Empty_or_Incompatible),
                 Miscellaneous_Failed,
                 Archive_Count,
                 Expanded_Count,
                 Filtered_Count,
                 Validation, 
                 Ingest_time,
                 index_size)
               VALUES (%(barcode)s,
                       %(index_name)s,
                       %(Index_Count)s,
                       %(Initial_Count)s,
                       %(Deduped_Count)s, 
                       %(Failed_(Password Protected_Empty_or_Incompatible))s,
                       %(Miscellaneous_Failed)s,
                       %(Archive_Count)s,
                       %(Expanded_Count)s,
                       %(Filtered_Count)s ),
                       %(Validation)s,
                       %(Ingest_time)s,
                       %(index_size)s
                       ;
            '''
        params = {'barcode': self.barcode,
                  'index_name': self.index,
                  'Index_Count': counts['Index Count'],
                  'Initial_Count':counts['Initial Count'],
                  'Deduped_Count':counts['Deduped Count'],
                  'Failed_(Password Protected_Empty_or_Incompatible)':counts['Failed (Password Protected, Empty or Incompatible)'],
                  'Miscellaneous_Failed':counts['Miscellaneous Failed'],
                  'Archive_Count':counts['Archive Count'],
                  'Expanded_Count':counts['Expanded Count'],
                  'Filtered_Count':counts['Filtered Count'],
                  'Validation': validate,
                  'Ingest_time': ingest_time,
                  'index_size': index_size}

        self.conn.insert(q, params)


if __name__ == "__main__":
    res = {}

    mdb = sql_connectors.PSQLConnector(host='127.0.0.1', port=5432, user='dustpan', database='dustpan')
    connection = elasticsearch.Elasticsearch(hosts=['10.40.40.56'], timeout=300)
    # create a object
    FC = FileCountCheck(None, None, mdb, connection, None, None)
    barcode_list = FC.get_barcode_list()
    FC.clear_table()
    for barcode in barcode_list:
        FC = FileCountCheck(barcode, None, mdb, connection, None, None)
        index_name = FC.get_index_name()
        system_type = FC.get_system_type()
        db_flavour = FC.get_db_flavour()
        counter = FileCountCheck(barcode, index_name, mdb, connection, system_type, db_flavour)
        counts = counter.get_all_counts()
        validate = counter.validate_count()
        ingest_time = counter.get_ingest_time()
        index_size = counter.get_index_size()
        # insert to table
        counter.save_qc_table(counts, validate,ingest_time,index_size)

    print('table saved')
