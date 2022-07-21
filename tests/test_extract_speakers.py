import unittest
from unittest import TestCase

from src.concall_tools import Speaker, get_speakers


class ExtractionTestCases(TestCase):
    def test_extract_speakers_aimco(self):
        pdf = "test_files/aimco-concall.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(name="Sayam Pokharna", firm="The Investment Lab"),
            # Ashit Dave is Executive Director and CFO, Missing CFO
            Speaker(name="Ashit Dave", firm="Executive Director"),
            Speaker(name="Navid Virani", firm="Bastion Capital"),
            Speaker(name="Ravi Sundaram", firm="Sundaram Family"),
            Speaker(name="Parth Agarwal", firm='individual investor'),
            Speaker(name="Vidya Verma", firm='individual investor'),
            Speaker(name="Nitin Gandhi", firm="KIFS Trade Capital"),
            Speaker(name="Milan Shah", firm="Urmil Research Consultancy"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_gpil(self):
        pdf = "test_files/gpil-concall.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(name="Ankit Toshniwal", firm="Go India Advisors"),
            Speaker(name="Dinesh Gandhi", firm="Director"),
            Speaker(name="Niteen Dharmavat", firm="Aurum Capital"),
            Speaker(name="Abhishek Agrawal", firm="Executive Director"),
            Speaker(name="Vikas Singh", firm="Philip Capital"),
            Speaker(name="Yogansh Jeswani", firm="Mittall Analytics"),
            Speaker(name="AM Lodha", firm="Sanmati Consultants"),
            Speaker(name="Ayush Mittal", firm="MAPL Value Investing Fund"),
            Speaker(name="Pritesh Chheda", firm="Lucky investment Managers"),
            Speaker(name="Anurag Patil", firm="Roha Asset Managers"),
            Speaker(name="Parthiv Shah", firm="Tracom Stock Brokers"),
            Speaker(name="Sanjay Bothra", firm='CFO'),
            # A and R International isn't parsed currently
            Speaker(name="Utsav Chhawchharia", firm="A and R International"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_tata_motors(self):
        pdf = "test_files/tata-motor.pdf"
        speakers = get_speakers(pdf)
        expected = [
            #Rearranged Order
            Speaker(name="PB Balaji", firm="GROUP CFO"),
            Speaker(name="Girish Wagh", firm="Executive Director"),
            Speaker(name="Shailesh Chandra", firm="MD"),
            Speaker(name="Adrian Mardell", firm="CFO"),
            Speaker(name="Thierry Bolloré", firm="CEO Jaguar Land Rover"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_lt(self):
        pdf = "test_files/lt.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            #P. Ramakrishnan is actually 'Head,', 'Investor', 'Relations,', 'Larsen', '&', 'Toubro', 'Limited.'
            Speaker(name="P. Ramakrishnan", firm="Head"),
            Speaker(name="Renu Baid", firm="IIFL"),
            Speaker(name="Sumit Kishore", firm="Axis Capital"),
            # Mohit Kumar is from DAM Capital
            # but it is missed as FROM is written as FORM in pdf
            Speaker(name="Mohit Kumar", firm="DAM Capital"),
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
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(name="C. Ramachandra Rao", firm="Joint Managing Director"),
            Speaker(name="Nitin Awasti", firm="Incread research"),
            Speaker(name="Sri C Ramachandra Rao", firm=None),
            Speaker(name="Sri Muthyam Reddy", firm=None),
            # Onkar Ghugadare is from Sree Investment
            # But it is missed because of spelling error in Ghugadre
            Speaker(name="Onkar Ghugadare", firm='Sree investment' ),
            Speaker(name="Sri. Alluri Nikhilesh", firm=None),
            Speaker(name="Vinayak Mohta", firm="Stallion Asset"),
            Speaker(name="Depesh Kashyap", firm="Equirus Capital"),
            Speaker(name="Ayush Mittal", firm="Mittal analytics"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_hdfc(self):
        pdf = "test_files/hdfc-concall.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(name="Srinivasan V", firm="Chief Financial Officer"),
            Speaker(name="Mahrukh Adajania", firm="Edelweiss"),
            Speaker(name="Rahul Jain", firm="Goldman Sachs"),
            Speaker(name="Aditya Jain", firm="Citigroup"),
            Speaker(name="Manish Shukla", firm="Axis Capital"),
            Speaker(name="Sagar Doshi", firm="Individual Investor"),
            Speaker(name="Adarsh Parasrampuria", firm="CLSA"),
            Speaker(name="Saurabh", firm="JP Morgan"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_asian_paints(self):
        pdf = "test_files/asian-paints.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(name="Arun Nair", firm="Corporate Communications"),
            Speaker(name="Amit Syngle", firm="MD & CEO"),
            Speaker(name="Avi Mehta", firm="Macquarie"),
            Speaker(name="Abneesh Roy", firm="Edelweiss"),
            Speaker(name="Shirish Pardeshi", firm="Centrum"),
            Speaker(name="Parag Rane", firm="GM-Finance"),
            Speaker(name="Saumil Mehta", firm="Kotak Life"),
            Speaker(name="Richard Liu", firm="JM Financial"),
            Speaker(name="Varun Singh", firm="IDBI Capital"),
            Speaker(name="Amit Sachdeva", firm="HSBC Securities"),
            Speaker(name="Percy Panthaki", firm="IIFL Securities"),
            Speaker(name="Sujay Kamath", firm="Millenium Partners"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_sandur(self):
        pdf = "test_files/sandur-concall.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(name="Bahirji Ghorpade", firm="Managing Director"),
            Speaker(name="Ayush Agarwal", firm="Mittal Analytics"),
            Speaker(name="Shubham Agarwal", firm="Equitas Investments"),
            Speaker(name="Abhay Lodha", firm=None),
            Speaker(name="Abhishek Maheshwari", firm=None),
            Speaker(name="Rahul Jain", firm="Systematix"),
            Speaker(name="Kamal Gupta", firm=None),
            Speaker(name="Ramesh Kumar Jain", firm='Accountant here from Bangalore'),
            Speaker(name="Ayush Mittal", firm="Mittal Analytics"),
            #Need to work on this
            Speaker(name="Ashok Kumar", firm='Dash – Company Secretary'),
            Speaker(name="Yachna Bhatia", firm=None),
            Speaker(name="Sahil Sanghvi", firm="Monarch Networth Capital"),
            Speaker(name="Mayur Shah", firm='Anand Rathi Portfolio Management team'),
            Speaker(name="Rajesh Agarwal", firm=None),
            Speaker(name="Abdul Saleem", firm='Director Mines.'),
            # sachin sanu is not found as his appearance is only once
            Speaker(name="Sachin Sanu", firm='Chief Financial Officer'),
            Speaker(name="Manoj Dua", firm=None),
            Speaker(name="Bach Raj Nahar", firm=None),
            #because Abdul is spelt incorreting to Abbdul somewhere
            Speaker(name='Abbdul Saleem', firm='Director Mines.'),
            Speaker(name="Arpit Ranka", firm='Investments'),
            Speaker(name="Jitendra Anchalia", firm=None),
            Speaker(name="Sanjay Jain", firm=None),
            Speaker(name="Hardik Jain", firm=None),
            Speaker(name="Prashanth Shah", firm=None),
            Speaker(name="Participant", firm=None),
            #Need to work on this
            Speaker(name="Satish Kumar", firm='Dash – Company Secretary'),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_hind_zinc(self):
        pdf = "test_files/hind-zinc.pdf"
        speakers = get_speakers(pdf)
        expected = [
            # Hindustan is a false positive
            #Speaker(name="Hindustan", firm=None),
            Speaker(name="Moderator", firm=None),
            Speaker(name="Shweta Arora", firm='Head of Investor Relations'),
            #following designation is wrong as persons designation is mentioned before the name
            Speaker(name="Arun Misra", firm='Interim CFO'),
            Speaker(name="Sandeep Modi", firm=None),
            Speaker(name="Amit Dixit", firm="Edelweiss"),
            Speaker(name="Anuj Singla", firm="Bank of America"),
            Speaker(name="Abhiram Iyer", firm="Deutsche CIB Center"),
            Speaker(
                name="Vishal Chandak", firm="Motilal Oswal Financial Services"
            ),
            # Vishal Chandak is written as Visha Chandak (the l is not in bold)
            #Speaker(name="Visha", firm=None),
            Speaker(name="Vikash Singh", firm="Phillip Capital"),
            Speaker(name="Ritesh Shah", firm="Investec"),
            Speaker(name="Abhijit Mitra", firm="ICICI Securities"),
            Speaker(
                name="Pallav Agarwal", firm="Antique Stock Broking Limited"
            ),
            Speaker(name="Rahul Jain", firm="Systematix"),
            Speaker(name="Saket Reddy", firm="Polsani Enterprises"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_eng_india(self):
        pdf = "test_files/eng-india.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(
                name="Kunal Sheth",
                firm="Batlivala &Karani Securities India Private Limited",
            ),
            Speaker(name="Vartika Shukla", firm='Chairman'),
            Speaker(name="Vinay Kalia", firm="Chief General Manager"),
            Speaker(name="Saket Kapoor", firm="Kapoor Industries"),
            Speaker(name="R.P. Batra", firm='Group General Manager'),
            Speaker(name="Viral Shah", firm="YES Securities"),
            Speaker(
                name="Sagar Gandhi",
                firm="Future Generali India Life Insurance Company",
            ),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_gsfc(self):
        pdf = "test_files/gsfc.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="V. D. Nanavaty", firm=None),
            Speaker(name="Moderator", firm=None),
            Speaker(name="Nirav Jimudia", firm="Anvil Research"),
            Speaker(name="Bharath Subramanian", firm="Sundaram Mutual Funds"),
            Speaker(name="Ahmed Madha", firm="Unifi Capital"),
            Speaker(name="Poojan Patel", firm="Mahadev Capital"),
            Speaker(name="Nishith Shah", firm="Equitus Investments"),
            Speaker(name="Saket Kapoor", firm="Kapoor & Company"),
            Speaker(name="S.P. Yadav", firm='Deputy Director'),
            Speaker(name="Deepak Chitroda", firm="Phillip Capital"),
            Speaker(name="Sreemant Dudhoria", firm="Unifi Capital"),
            Speaker(name="Priya Mehta", firm="Rishi Finstock"),
            Speaker(name="Falguni Dutta", firm="Jet Age Securities"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_tcs(self):
        pdf = "test_files/tcs.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None),
            Speaker(name="Kedar Shirali", firm="Global Head"),
            Speaker(name="Rajesh Gopinathan", firm='Chief Executive Officer'),
            Speaker(name="Samir Seksaria", firm='Chief Financial Officer'),
            Speaker(name="N.G. Subramaniam", firm='Chief Operating Officer'),
            Speaker(name="Kumar Rakesh", firm="BNP Paribas"),
            Speaker(name="Diviya Nagarajan", firm="UBS"),
            Speaker(name="Sandip Agarwal", firm="Edelweiss"),
            Speaker(name="Apurva Prasad", firm="HDFC Securities"),
            Speaker(
                name="Mukul Garg", firm="Motilal Oswal Financial Services"
            ),
            Speaker(name="Sandeep Shah", firm="Equirus Securities"),
            Speaker(name="Ravi Menon", firm="Macquarie"),
            # Samir Seksaria is not found as his appearance is only once
            Speaker(name="Gaurav Rateria", firm="Morgan Stanley"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)


if __name__ == "__main__":
    unittest.main()
