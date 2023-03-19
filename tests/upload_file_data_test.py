import tempfile
from django.test import TestCase, override_settings

from django.core.files.uploadedfile import SimpleUploadedFile
from api.models import User

from api.upload_file_data import get_rows, handle_uploaded_file

class TestGetRows(TestCase):
    def tearDown(self):
        self._fixture_teardown()

    def test_csv(self):
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            f.write(b'first_name,last_name,national_id,birth_date,address,country,phone_number,email\n')
            f.write(b'John,Doe,123456789,1980-01-01,123 Main St,USA,123-456-7890,john.doe@example.com\n')
            f.write(b'Jane,Smith,987654321,1985-05-05,456 Elm St,USA,987-654-3210,jane.smith@example.com\n')

        df = get_rows(2, 0, f)
        self.assertEqual(df.iloc[0]['first_name'], 'John')
        self.assertEqual(df.iloc[1]['email'], 'jane.smith@example.com')

        f.close()

    def test_json(self):
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            f.write(b'{"first_name": "John", "last_name": "Doe", "national_id": "123456789", "birth_date": "1980-01-01", "address": "123 Main St", "country": "USA", "phone_number": "123-456-7890", "email": "john.doe@example.com"}\n')
            f.write(b'{"first_name": "Jane", "last_name": "Smith", "national_id": "987654321", "birth_date": "1985-05-05", "address": "456 Elm St", "country": "USA", "phone_number": "987-654-3210", "email": "jane.smith@example.com"}\n')

        df = get_rows(2, 0, f)
        self.assertEqual(df.iloc[0]['first_name'], 'John')
        self.assertEqual(df.iloc[1]['email'], 'jane.smith@example.com')

        f.close()

    def test_xml(self):
        # create sample XML file
        xml_data = """
            <users>
                <user>
                    <first_name>John</first_name>
                    <last_name>Doe</last_name>
                    <national_id>123456</national_id>
                    <birth_date>1990-01-01</birth_date>
                    <address>123 Main St.</address>
                    <country>USA</country>
                    <phone_number>555-1234</phone_number>
                    <email>john.doe@example.com</email>
                </user>
                <user>
                    <first_name>Jane</first_name>
                    <last_name>Smith</last_name>
                    <national_id>654321</national_id>
                    <birth_date>1995-02-01</birth_date>
                    <address>456 Elm St.</address>
                    <country>Canada</country>
                    <phone_number>555-5678</phone_number>
                    <email>jane.smith@example.com</email>
                </user>
            </users>
        """
        xml_file = SimpleUploadedFile("test.xml", xml_data.encode("utf-8"))

        # call get_rows function
        df = get_rows(steps=2, count=0, file=xml_file)

        # check that the correct data was extracted
        assert len(df) == 2
        assert df.iloc[0]["first_name"] == "John"
        assert df.iloc[1]["national_id"] == "654321"
    
    def test_xls(self):
        # create sample XLSX file
        xlsx_data = """
            first_name	last_name	national_id	birth_date	address	country	phone_number	email
            John	Doe	123456	1990-01-01	123 Main St.	USA	555-1234	john.doe@example.com
            Jane	Smith	654321	1995-02-01	456 Elm St.	Canada	555-5678	jane.smith@example.com
        """
        xlsx_file = SimpleUploadedFile("test.xlsx", xlsx_data.encode("utf-8"))

        # call get_rows function
        df = get_rows(steps=2, count=0, file=xlsx_file)

        # check that the correct data was extracted
        assert len(df) == 2
        assert df.iloc[0]["first_name"] == "John"
        assert df.iloc[1]["national_id"] == "654321"

    
    def test_txt(self):
        # create sample TXT file
        txt_data = """
            John Doe 123456 1990-01-01 123 Main St. USA 555-1234 john.doe@example.com
            Jane Smith 654321 1995-02-01 456 Elm St. Canada 555-5678 jane.smith@example.com
        """
        txt_file = SimpleUploadedFile("test.txt", txt_data.encode("utf-8"))

        # call get_rows function
        df = get_rows(steps=2, count=0, file=txt_file)

        # check that the correct data was extracted
        assert len(df) == 2
        assert df.iloc[0]["first_name"] == "John"
        assert df.iloc[1]["national_id"] == "654321"


class TestTxtFileProcessing(TestCase):
    def tearDown(self):
        self._fixture_teardown()

    @override_settings(DEBUG=True)
    def test_txt_file_processing(self):
        # Define test data
        data = "John Smith 123456789 1990-01-01 123 Main St USA +1-123-456-7890 john.smith@example.com"
        txt_file = SimpleUploadedFile("test_data.txt", data.encode())

        # Call the function to be tested
        handle_uploaded_file(txt_file)

        # Assert that the users were created in the database
        self.assertEqual(User.objects.count(), 1)

        # Assert the user's data
        user = User.objects.first()
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Smith")
        self.assertEqual(user.national_id, "123456789")
        self.assertEqual(str(user.birth_date), "1990-01-01")
        self.assertEqual(user.address, "123 Main St")
        self.assertEqual(user.country, "USA")
        self.assertEqual(user.phone_number, "+1-123-456-7890")
        self.assertEqual(user.email, "john.smith@example.com")
