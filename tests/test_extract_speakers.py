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
            Speaker(name="Abhishek Agrawal", firm=None),
            Speaker(name="Vikas Singh", firm="Philip Capital"),
            Speaker(name="Yogansh Jeswani", firm="Mittall Analytics"),
            Speaker(name="AM Lodha", firm="Sanmati Consultants"),
            Speaker(name="Ayush Mittal", firm="MAPL Value Investing Fund"),
            Speaker(name="Pritesh Chheda", firm="Lucky investment Managers"),
            Speaker(name="Anurag Patil", firm="Roha Asset Managers"),
            Speaker(name="Parthiv Shah", firm="Tracom Stock Brokers"),
            Speaker(name="Sanjay Bothra", firm=None),
            # A and R International isn't parsed currently
            Speaker(name="Utsav Chhawchharia", firm="A"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_tata_motors(self):
        pdf = "test_files/tata-motor.pdf"
        speakers = extract_speakers(pdf)
        expected = [
            Speaker(name="Sneha Gavankar", firm=None),
            Speaker(name="PB Balaji", firm=None),
            Speaker(name="Adrian Mardell", firm=None),
            Speaker(name="Girish Wagh", firm=None),
            Speaker(name="Shailesh Chandra", firm=None),
            Speaker(name="Thierry Bolloré", firm=None),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)


if __name__ == "__main__":
    unittest.main()
