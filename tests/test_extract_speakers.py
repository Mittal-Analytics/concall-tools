import unittest
from unittest import TestCase

from src.concall_tools.extract_speakers import Speaker, extract_speakers


class ExtractionTestCases(TestCase):
    def test_extract_speakers_aimco(self):
        pdf = "test_files/aimco-concall.pdf"
        speakers = extract_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(name="Sayam Pokharna", firm="Investment Lab"),
            Speaker(name="Ashit Dave", firm=None),
            Speaker(name="Navid Virani", firm="Bastion Capital"),
            Speaker(name="Ravi Sundaram", firm="Sundaram Family"),
            Speaker(name="Parth Agarwal", firm=None),
            Speaker(name="Vidya Verma", firm=None),
            Speaker(name="Nitin Gandhi", firm="KIFS Trade Capital"),
            Speaker(name="Milan Shah", firm="Urmil Research Consultancy"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_gpil(self):
        pdf = "test_files/gpil-concall.pdf"
        speakers = extract_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(name="Ankit Toshniwal", firm="Go India Advisors"),
            Speaker(name="Dinesh Gandhi", firm="GPIL"),
            Speaker(name="Niteen Dharmavat", firm="Aurum Capital"),
            Speaker(name="Abhishek Agrawal", firm="Executive Director"),
            Speaker(name="Vikas Singh", firm="Philip Capital"),
            Speaker(name="Yogansh Jeswani", firm="Mittall Analytics"),
            Speaker(name="AM Lodha", firm="Sanmati Consultants"),
            Speaker(name="Ayush Mittal", firm="MAPL Value Investing Fund"),
            Speaker(name="Pritesh Chheda", firm="Lucky investment Managers"),
            Speaker(name="Anurag Patil", firm="Roha Asset Managers"),
            Speaker(name="Parthiv Shah", firm="Tracom Stock Brokers"),
            Speaker(name="Sanjay Bothra", firm=None),
            # A and R International isn't parsed currently
            Speaker(name="Utsav Chhawchharia", firm="A and R International"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_tata_motors(self):
        pdf = "test_files/tata-motor.pdf"
        speakers = extract_speakers(pdf)
        expected = [
            Speaker(name="Sneha Gavankar", firm=None),
            Speaker(name="PB Balaji", firm="Group CFO"),
            Speaker(name="Adrian Mardell", firm="CFO"),
            Speaker(name="Girish Wagh", firm="Executive Director"),
            Speaker(name="Shailesh Chandra", firm="MD"),
            Speaker(name="Thierry Bolloré", firm="CEO Jaguar Land Rover"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_lt(self):
        pdf = "test_files/lt.pdf"
        speakers = extract_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(name="P. Ramakrishnan", firm=None),
            Speaker(name="Renu Baid", firm="IIFL"),
            Speaker(name="Sumit Kishore", firm="Axis Capital"),
            # Mohit Kumar is from DAM Capital
            # but it is missed as FROM is written as FORM in pdf
            Speaker(name="Mohit Kumar", firm=None),
            Speaker(name="Ankur Sharma", firm="HDFC Life"),
            Speaker(name="Puneet Gulati", firm="HSBC"),
            Speaker(name="Nitin Arora", firm="Axis Mutual Fund"),
            Speaker(name="Parikshit Khandpal", firm="HDFC Securities"),
            Speaker(name="Amish Shah", firm="Bank of America Securities"),
            Speaker(name="Ashish Shah", firm="Centrum Broking"),
            Speaker(name="Kirti Jain", firm="Canara HSBC Life"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_avanti(self):
        pdf = "test_files/avanti.pdf"
        speakers = extract_speakers(pdf)
        expected = [
            Speaker(name="C. Ramachandra Rao", firm="Joint Managing Director"),
            # these two headings are false-positives
            # because they are in bold, just like names
            Speaker(name="SHRIMP FEED CONSUMPTION", firm=None),
            Speaker(name="SHRIMP PROCESSING AND EXPORT", firm=None),
            Speaker(name="Moderator", firm=None),
            Speaker(name="Nitin Awasti", firm="Incread research"),
            Speaker(name="Sri C Ramachandra Rao", firm=None),
            Speaker(name="Sri Muthyam Reddy", firm=None),
            # Onkar Ghugadare is from Sree Investment
            # But it is missed because of spelling error in Ghugadre
            Speaker(name="Onkar Ghugadare", firm=None),
            Speaker(name="Sri. Alluri Nikhilesh", firm=None),
            Speaker(name="Vinayak Mohta", firm="Stallion Asset"),
            Speaker(name="Depesh Kashyap", firm="Equirus Capital"),
            Speaker(name="Ayush Mittal", firm="Mittal analytics"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_hdfc(self):
        pdf = "test_files/hdfc-concall.pdf"
        speakers = extract_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(name="Srinivasan V", firm=None),
            Speaker(name="Mahrukh Adajania", firm="Edelweiss"),
            Speaker(name="Rahul Jain", firm="Goldman Sachs"),
            Speaker(name="Aditya Jain", firm="Citigroup"),
            Speaker(name="Manish Shukla", firm="Axis Capital"),
            Speaker(name="Sagar Doshi", firm=None),
            Speaker(name="Adarsh Parasrampuria", firm="CLSA"),
            Speaker(name="Saurabh", firm="JP Morgan"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_asian_paints(self):
        pdf = "test_files/asian-paints.pdf"
        speakers = extract_speakers(pdf)
        expected = [
            Speaker(name="Arun Nair", firm="Corporate Communications"),
            Speaker(name="Amit Syngle", firm=None),
            Speaker(name="Avi Mehta", firm="Macquarie"),
            Speaker(name="Abneesh Roy", firm="Edelweiss"),
            Speaker(name="Shirish Pardeshi", firm="Centrum"),
            Speaker(name="Saumil Mehta", firm="Kotak Life"),
            Speaker(name="Richard Liu", firm="JM Financial"),
            Speaker(name="Varun Singh", firm="IDBI Capital"),
            Speaker(name="Amit Sachdeva", firm="HSBC Securities"),
            Speaker(name="Percy Panthaki", firm="IIFL Securities"),
            Speaker(name="Sujay Kamath", firm="Millenium Partners"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)


if __name__ == "__main__":
    unittest.main()
