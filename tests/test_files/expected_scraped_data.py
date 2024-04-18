expected_scraped_data = {}

expected_scraped_data["Victims by Age Group"] = {
    "Age_Range": ["Under 20", "20 - 29", "30 - 39", "40 - 49", "50 - 59", "Over 60"],
    "Count": [140, 560, 661, 675, 670, 669],
    "Amount_Loss": [80752, 507699, 414557, 1150530, 2203766, 2389124],
    "year": [2016, 2016, 2016, 2016, 2016, 2016],
    "state_name": ["Alabama", "Alabama", "Alabama", "Alabama", "Alabama", "Alabama"]
}

expected_scraped_data["Crime Type by Victim Loss"] = [
    {"Crime_Type": "419/Overpayment", "Loss_Amount": 299145, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Advanced Fee", "Loss_Amount": 763289, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Auction", "Loss_Amount": 145638, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "BEC/EAC", "Loss_Amount": 1739162, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Charity", "Loss_Amount": 910, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Civil Matter", "Loss_Amount": 29398, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Confidence Fraud/Romance", "Loss_Amount": 1660271, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Corporate Data Breach", "Loss_Amount": 20080, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Credit Card Fraud", "Loss_Amount": 293019, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Crimes Against Children", "Loss_Amount": 14600, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Criminal Forums", "Loss_Amount": 0, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Denial of Service", "Loss_Amount": 35, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Employment", "Loss_Amount": 244906, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Extortion", "Loss_Amount": 80659, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Gambling", "Loss_Amount": 0, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Government Impersonation", "Loss_Amount": 59148, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Hacktivist", "Loss_Amount": 0, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Harassment/Threats of Violence", "Loss_Amount": 50859, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Health Care Related", "Loss_Amount": 290, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "IPR/Copyright and Counterfeit", "Loss_Amount": 27937, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Identity Theft", "Loss_Amount": 372269, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Investment", "Loss_Amount": 237630, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Lottery/Sweepstakes", "Loss_Amount": 109757, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Malware/Scareware", "Loss_Amount": 6122, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Misrepresentation", "Loss_Amount": 63936, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "No Lead Value", "Loss_Amount": 0, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Non-payment/Non-Delivery", "Loss_Amount": 1269330, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Other", "Loss_Amount": 65343, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Personal Data Breach", "Loss_Amount": 619807, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Phishing/Vishing/Smishing/Pharming", "Loss_Amount": 412604, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Ransomware", "Loss_Amount": 5001, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Re-shipping", "Loss_Amount": 2611, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Real Estate/Rental", "Loss_Amount": 107620, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Tech Support", "Loss_Amount": 90738, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Terrorism", "Loss_Amount": 0, "year": 2016, "state_name": "Alabama"},
    {"Crime_Type": "Virus", "Loss_Amount": 1778, "year": 2016, "state_name": "Alabama"}
]


expected_scraped_data["expected_merged_data"] = [
    {"Age_Range": "Under 20", "Count": 140, "Amount_Loss": 80752, "year": 2016, "state_name": "Alabama"},
    {"Age_Range": "20 - 29", "Count": 560, "Amount_Loss": 507699, "year": 2016, "state_name": "Alabama"},
    {"Age_Range": "30 - 39", "Count": 661, "Amount_Loss": 414557, "year": 2016, "state_name": "Alabama"},
    {"Age_Range": "40 - 49", "Count": 675, "Amount_Loss": 1150530, "year": 2016, "state_name": "Alabama"},
    {"Age_Range": "50 - 59", "Count": 670, "Amount_Loss": 2203766, "year": 2016, "state_name": "Alabama"},
    {"Age_Range": "Over 60", "Count": 669, "Amount_Loss": 2389124, "year": 2016, "state_name": "Alabama"},
    {"Age_Range": "Under 20", "Count": 140, "Amount_Loss": 80752, "year": 2017, "state_name": "Alabama"},
    {"Age_Range": "20 - 29", "Count": 560, "Amount_Loss": 507699, "year": 2017, "state_name": "Alabama"},
    {"Age_Range": "30 - 39", "Count": 661, "Amount_Loss": 414557, "year": 2017, "state_name": "Alabama"},
    {"Age_Range": "40 - 49", "Count": 675, "Amount_Loss": 1150530, "year": 2017, "state_name": "Alabama"},
    {"Age_Range": "50 - 59", "Count": 670, "Amount_Loss": 2203766, "year": 2017, "state_name": "Alabama"},
    {"Age_Range": "Over 60", "Count": 669, "Amount_Loss": 2389124, "year": 2017, "state_name": "Alabama"}
]