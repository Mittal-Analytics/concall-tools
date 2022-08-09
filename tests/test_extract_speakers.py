import unittest
from unittest import TestCase

from src.concall_tools import Speaker_with_is_management, get_speakers
Speaker=Speaker_with_is_management

class ExtractionTestCases(TestCase):
    def test_extract_speakers_aimco(self):
        pdf = "test_files/aimco-concall.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None, is_management="No"),
            Speaker(name="Sayam Pokharna", firm="The Investment Lab",is_management="No"),
            # Ashit Dave is Executive Director and CFO, Missing CFO
            Speaker(name="Ashit Dave", firm="Executive Director", is_management="Yes"),
            Speaker(name="Navid Virani", firm="Bastion Capital", is_management="No"),
            Speaker(name="Ravi Sundaram", firm="Sundaram Family", is_management="No"),
            Speaker(name="Parth Agarwal", firm='individual investor', is_management="No"),
            Speaker(name="Vidya Verma", firm='individual investor', is_management="No"),
            Speaker(name="Nitin Gandhi", firm="KIFS Trade Capital", is_management="No"),
            Speaker(name="Milan Shah", firm="Urmil Research Consultancy", is_management="No"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_gpil(self):
        pdf = "test_files/gpil-concall.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None, is_management="No"), 
            Speaker(name="Ankit Toshniwal", firm="Go India Advisors", is_management="No"),
            Speaker(name="Dinesh Gandhi", firm="Director", is_management="Yes"),
            Speaker(name="Niteen Dharmavat", firm="Aurum Capital", is_management="No"),
            Speaker(name="Abhishek Agrawal", firm="Executive Director", is_management="Yes"),
            Speaker(name="Vikas Singh", firm="Philip Capital", is_management="No"),
            Speaker(name="Yogansh Jeswani", firm="Mittall Analytics", is_management="No"),
            Speaker(name="AM Lodha", firm="Sanmati Consultants", is_management="No"),
            Speaker(name="Ayush Mittal", firm="MAPL Value Investing Fund", is_management="No"),
            Speaker(name="Pritesh Chheda", firm="Lucky investment Managers", is_management="No"),
            Speaker(name="Anurag Patil", firm="Roha Asset Managers", is_management="No"),
            Speaker(name="Parthiv Shah", firm="Tracom Stock Brokers", is_management="No"),
            Speaker(name="Sanjay Bothra", firm='CFO', is_management="Yes"),
            Speaker(name="Utsav Chhawchharia", firm="A and R International", is_management="No"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_tata_motors(self):
        pdf = "test_files/tata-motor.pdf"
        speakers = get_speakers(pdf)
        expected = [
            #Rearranged Order
            Speaker(name="PB Balaji", firm="GROUP CFO", is_management="Yes"),
            Speaker(name="Girish Wagh", firm="Executive Director", is_management="Yes"),
            Speaker(name="Shailesh Chandra", firm="MD", is_management="Yes"),
            Speaker(name="Adrian Mardell", firm="CFO", is_management="Yes"),
            Speaker(name="Thierry Bolloré", firm="CEO Jaguar Land Rover", is_management="Yes"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_lt(self):
        pdf = "test_files/lt.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None, is_management="No"),
            #P. Ramakrishnan is actually 'Head,', 'Investor', 'Relations,', 'Larsen', '&', 'Toubro', 'Limited.'
            Speaker(name="P. Ramakrishnan", firm="Head", is_management="Yes"),
            Speaker(name="Renu Baid", firm="IIFL", is_management="No"),
            Speaker(name="Sumit Kishore", firm="Axis Capital", is_management="No"),
            # Mohit Kumar is from DAM Capital
            # but it is missed as FROM is written as FORM in pdf
            Speaker(name="Mohit Kumar", firm="DAM Capital", is_management="No"),
            Speaker(name="Ankur Sharma", firm="HDFC Life", is_management="No"),
            Speaker(name="Puneet Gulati", firm="HSBC", is_management="No"),
            Speaker(name="Nitin Arora", firm="Axis Mutual Fund", is_management="No"),
            Speaker(name="Parikshit Khandpal", firm="HDFC Securities", is_management="No"),
            Speaker(name="Amish Shah", firm="Bank of America Securities", is_management="No"),
            Speaker(name="Ashish Shah", firm="Centrum Broking", is_management="No"),
            Speaker(name="Kirti Jain", firm="Canara HSBC Life", is_management="No"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_avanti(self):
        pdf = "test_files/avanti.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None, is_management="No"),
            Speaker(name="C. Ramachandra Rao", firm="Joint Managing Director", is_management="Yes"),
            Speaker(name="Nitin Awasti", firm="Incread research", is_management="No"),
            Speaker(name="Sri C Ramachandra Rao", firm=None, is_management="Yes"),
            Speaker(name="Sri Muthyam Reddy", firm=None, is_management="No"),
            # Onkar Ghugadare is from Sree Investment
            # But it is missed because of spelling error in Ghugadre
            Speaker(name="Onkar Ghugadare", firm='Sree investment' , is_management="No"),
            Speaker(name="Sri. Alluri Nikhilesh", firm='Executive Director - Avanti Frozen Foods Pvt Ltd', is_management="Yes"),
            Speaker(name="Vinayak Mohta", firm="Stallion Asset", is_management="No"),
            Speaker(name="Depesh Kashyap", firm="Equirus Capital", is_management="No"),
            Speaker(name="Ayush Mittal", firm="Mittal analytics", is_management="No"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_hdfc(self):
        pdf = "test_files/hdfc-concall.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None, is_management="No"),
            Speaker(name="Srinivasan V", firm="Chief Financial Officer", is_management="Yes"),
            Speaker(name="Mahrukh Adajania", firm="Edelweiss", is_management="No"),
            Speaker(name="Rahul Jain", firm="Goldman Sachs", is_management="No"),
            Speaker(name="Aditya Jain", firm="Citigroup", is_management="No"),
            Speaker(name="Manish Shukla", firm="Axis Capital", is_management="No"),
            Speaker(name="Sagar Doshi", firm="Individual Investor", is_management="No"),
            Speaker(name="Adarsh Parasrampuria", firm="CLSA", is_management="No"), 
            Speaker(name="Saurabh", firm="JP Morgan", is_management="No"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_asian_paints(self):
        pdf = "test_files/asian-paints.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None, is_management='No'),
            Speaker(name="Arun Nair", firm="Corporate Communications", is_management="Yes"),
            Speaker(name="Amit Syngle", firm="MD & CEO", is_management="Yes"),
            Speaker(name="Avi Mehta", firm="Macquarie", is_management="No",),
            Speaker(name="Abneesh Roy", firm="Edelweiss", is_management="No"),
            Speaker(name="Shirish Pardeshi", firm="Centrum", is_management="No"),
            Speaker(name="Parag Rane", firm="GM-Finance", is_management="Yes"),
            Speaker(name="Saumil Mehta", firm="Kotak Life", is_management="No"),
            Speaker(name="Richard Liu", firm="JM Financial", is_management="No"), 
            Speaker(name="Varun Singh", firm="IDBI Capital", is_management="No"), 
            Speaker(name="Amit Sachdeva", firm="HSBC Securities", is_management="No"),
            Speaker(name="Percy Panthaki", firm="IIFL Securities", is_management="No"),
            Speaker(name="Sujay Kamath", firm="Millenium Partners", is_management="No"), 
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_sandur(self):
        pdf = "test_files/sandur-concall.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None, is_management='No'),
            Speaker(name="Bahirji Ghorpade", firm="Managing Director", is_management="Yes"),
            Speaker(name="Ayush Agarwal", firm="Mittal Analytics", is_management="No"),
            Speaker(name="Shubham Agarwal", firm="Equitas Investments", is_management="No"),
            Speaker(name="Abhay Lodha", firm=None, is_management="No"), 
            Speaker(name="Abhishek Maheshwari", firm=None, is_management="No"),
            Speaker(name="Rahul Jain", firm="Systematix", is_management="No"),
            Speaker(name="Kamal Gupta", firm=None, is_management="No"),
            #Ramesh kumar Jain is "Chartered accountant here from Banglore" which is not identified as a firm
            Speaker(name="Ramesh Kumar Jain", firm=None, is_management="No"),
            Speaker(name="Ayush Mittal", firm="Mittal Analytics", is_management="No"),
            Speaker(name="Ashok Kumar", firm=None, is_management="No"),
            Speaker(name="Yachna Bhatia", firm=None, is_management="No"),
            Speaker(name="Sahil Sanghvi", firm="Monarch Networth Capital", is_management="No"),
            Speaker(name="Mayur Shah", firm='Anand Rathi Portfolio Management team', is_management="No"),
            Speaker(name="Rajesh Agarwal", firm=None, is_management="No"),
            Speaker(name="Abdul Saleem", firm='Director Mines', is_management="Yes"),
            # sachin sanu is not found as his appearance is only once
            Speaker(name="Sachin Sanu", firm='Chief Financial Officer', is_management="Yes"),
            Speaker(name="Manoj Dua", firm=None, is_management="No"),
            Speaker(name="Bach Raj Nahar", firm=None, is_management="No"),
            #because Abdul is spelt incorreting to Abbdul somewhere
            #Speaker(name='Abbdul Saleem', firm='Director Mines.', is_management="Yes"),
            Speaker(name="Arpit Ranka", firm='Investments', is_management="No"),
            Speaker(name="Jitendra Anchalia", firm=None, is_management="No"),
            Speaker(name="Sanjay Jain", firm=None, is_management="No"), 
            Speaker(name="Hardik Jain", firm=None, is_management="No"),
            Speaker(name="Prashanth Shah", firm=None, is_management="No"),
            Speaker(name="Participant", firm=None, is_management="No"), 
            Speaker(name="Satish Kumar", firm=None, is_management="No"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_hind_zinc(self):
        pdf = "test_files/hind-zinc.pdf"
        speakers = get_speakers(pdf)
        expected = [
            # Hindustan is a false positive
            #Speaker(name="Hindustan", firm=None),
            Speaker(name="Moderator", firm=None, is_management="No"),
            Speaker(name="Shweta Arora", firm='Head of Investor Relations', is_management="Yes"),
            #following designation is wrong as persons designation is mentioned before the name
            Speaker(name="Arun Misra", firm='Interim CFO', is_management="Yes"),
            Speaker(name="Sandeep Modi", firm=None, is_management="Yes"),
            Speaker(name="Amit Dixit", firm="Edelweiss", is_management="No"),
            Speaker(name="Anuj Singla", firm="Bank of America", is_management="No"), 
            Speaker(name="Abhiram Iyer", firm="Deutsche CIB Center", is_management="No"),
            Speaker(
                name="Vishal Chandak", firm="Motilal Oswal Financial Services", is_management="No"
            ),
            # Vishal Chandak is written as Visha Chandak (the l is not in bold)
            #Speaker(name="Visha", firm=None),
            Speaker(name="Vikash Singh", firm="Phillip Capital", is_management="No"), 
            Speaker(name="Ritesh Shah", firm="Investec", is_management="No"),
            Speaker(name="Abhijit Mitra", firm="ICICI Securities", is_management="No"),
            Speaker(
                name="Pallav Agarwal", firm="Antique Stock Broking Limited", is_management="No"
            ),
            Speaker(name="Rahul Jain", firm="Systematix", is_management="No"),
            Speaker(name="Saket Reddy", firm="Polsani Enterprises", is_management="No"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_eng_india(self):
        pdf = "test_files/eng-india.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None, is_management="No"),
            Speaker(
                name="Kunal Sheth",
                firm="Batlivala &Karani Securities India Private Limited", is_management="No"
            ),
            Speaker(name="Vartika Shukla", firm='Chairman', is_management="Yes"),
            Speaker(name="Vinay Kalia", firm="Chief General Manager", is_management="Yes"),
            Speaker(name="Saket Kapoor", firm="Kapoor Industries", is_management="No"),
            Speaker(name="R.P. Batra", firm='Group General Manager', is_management="Yes"),
            Speaker(name="Viral Shah", firm="YES Securities", is_management="No"),
            Speaker(
                name="Sagar Gandhi",
                firm="Future Generali India Life Insurance Company", is_management="No"
            ),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_gsfc(self):
        pdf = "test_files/gsfc.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="V. D. Nanavaty", firm=None, is_management="Yes"),
            Speaker(name="Moderator", firm=None, is_management="No"),
            Speaker(name="Nirav Jimudia", firm="Anvil Research", is_management="No"),
            Speaker(name="Bharath Subramanian", firm="Sundaram Mutual Funds", is_management="No"),
            Speaker(name="Ahmed Madha", firm="Unifi Capital", is_management="No"),
            Speaker(name="Poojan Patel", firm="Mahadev Capital", is_management="No"),
            Speaker(name="Nishith Shah", firm="Equitus Investments", is_management="No"),
            Speaker(name="Saket Kapoor", firm="Kapoor & Company", is_management="No"),
            Speaker(name="S.P. Yadav", firm='Deputy Director', is_management="Yes"),
            Speaker(name="Deepak Chitroda", firm="Phillip Capital", is_management="No"),
            Speaker(name="Sreemant Dudhoria", firm="Unifi Capital", is_management="No"),
            Speaker(name="Priya Mehta", firm="Rishi Finstock", is_management="No"),
            Speaker(name="Falguni Dutta", firm="Jet Age Securities", is_management="No"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)

    def test_extract_speakers_tcs(self):
        pdf = "test_files/tcs.pdf"
        speakers = get_speakers(pdf)
        expected = [
            Speaker(name="Moderator", firm=None, is_management="No"),
            Speaker(name="Kedar Shirali", firm="Global Head", is_management="Yes"),
            Speaker(name="Rajesh Gopinathan", firm='Chief Executive Officer', is_management="Yes"),
            Speaker(name="Samir Seksaria", firm='Chief Financial Officer', is_management="Yes"),
            Speaker(name="N.G. Subramaniam", firm='Chief Operating Officer', is_management="Yes"),
            Speaker(name="Kumar Rakesh", firm="BNP Paribas", is_management="No"),
            Speaker(name="Diviya Nagarajan", firm="UBS", is_management="No"),
            Speaker(name="Sandip Agarwal", firm="Edelweiss", is_management="No"),
            Speaker(name="Apurva Prasad", firm="HDFC Securities", is_management="No"),
            Speaker(
                name="Mukul Garg", firm="Motilal Oswal Financial Services", is_management="No"
            ),
            Speaker(name="Sandeep Shah", firm="Equirus Securities", is_management="No"),
            Speaker(name="Ravi Menon", firm="Macquarie", is_management="No"),
            Speaker(name="Gaurav Rateria", firm="Morgan Stanley", is_management="No"),
        ]
        self.maxDiff = None
        self.assertEqual(speakers, expected)


if __name__ == "__main__":
    unittest.main()
