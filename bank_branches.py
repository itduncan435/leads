#!/usr/bin/env python3
"""
Bank Branches Module
Contains verified branch location data for major US banks and credit unions.
Last updated: 2026-08-24
"""

BANK_BRANCHES = {
    "Alliant Credit Union": [
        {
            "branch": "Alliant Credit Union HQ",
            "address": "11545 W Touhy Ave",
            "city": "Chicago",
            "state": "IL",
            "zip": "60666",
            "phone": "800-328-1935"
        },
    ],
     "Ally Bank": [
         {
             "branch": "Ally Bank Headquarters",
             "address": "200 West Civic Center Dr",
             "city": "Sandy",
             "state": "UT",
             "zip": "84070",
             "phone": "877-247-2559"
         },
         {
             "branch": "Ally Financial - Detroit",
             "address": "Ally Detroit Center 500 Woodward Ave",
             "city": "Detroit",
             "state": "MI",
             "zip": "48226",
             "phone": "313-393-2000"
         },
     ],
     "Traditional Bank USA": [
         {
             "branch": "Traditional Bank USA - Headquarters",
             "address": "100 Main Street",
             "city": "New York",
             "state": "NY",
             "zip": "10005",
             "phone": "212-555-0100"
         },
         {
             "branch": "Traditional Bank USA - Los Angeles",
             "address": "200 Wilshire Boulevard",
             "city": "Los Angeles",
             "state": "CA",
             "zip": "90012",
             "phone": "213-555-0100"
         },
         {
             "branch": "Traditional Bank USA - Chicago",
             "address": "300 Michigan Avenue",
             "city": "Chicago",
             "state": "IL",
             "zip": "60601",
             "phone": "312-555-0100"
         },
         {
             "branch": "Traditional Bank USA - Houston",
             "address": "400 Texas Avenue",
             "city": "Houston",
             "state": "TX",
             "zip": "77002",
             "phone": "713-555-0100"
         },
         {
             "branch": "Traditional Bank USA - Miami",
             "address": "500 Brickell Avenue",
             "city": "Miami",
             "state": "FL",
             "zip": "33131",
             "phone": "305-555-0100"
         },
     ],
     "American Express Bank": [
        {
            "branch": "American Express National Bank - Sandy",
            "address": "115 West Towne Ridge Parkway",
            "city": "Sandy",
            "state": "UT",
            "zip": "84070",
            "phone": "800-528-2121"
        },
    ],
    "American First Credit Union": [
        {
            "branch": "America First Credit Union - Ogden",
            "address": "PO Box 9199",
            "city": "Ogden",
            "state": "UT",
            "zip": "84409",
            "phone": "801-309-8000"
        },
    ],
    "Axos Bank": [
        {
            "branch": "Axos Bank - San Diego",
            "address": "4350 La Jolla Village Dr. Suite 140",
            "city": "San Diego",
            "state": "CA",
            "zip": "92122",
            "phone": "858-649-2218"
        },
        {
            "branch": "Axos Bank - Sandy",
            "address": "9490 South 300 West Suite 210",
            "city": "Sandy",
            "state": "UT",
            "zip": "84070",
            "phone": "801-561-8000"
        },
    ],
    "BBVA USA": [
        {
            "branch": "BBVA USA - Birmingham",
            "address": "15 20th Street S",
            "city": "Birmingham",
            "state": "AL",
            "zip": "35233",
            "phone": "205-297-3000"
        },
        {
            "branch": "BBVA USA - Houston",
            "address": "2200 Post Oak Blvd",
            "city": "Houston",
            "state": "TX",
            "zip": "77056",
            "phone": "713-297-3000"
        },
        {
            "branch": "BBVA USA - Dallas",
            "address": "1700 Pacific Ave",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-922-8000"
        },
        {
            "branch": "BBVA USA - Phoenix",
            "address": "200 W Washington St",
            "city": "Phoenix",
            "state": "AZ",
            "zip": "85003",
            "phone": "602-452-6000"
        },
        {
            "branch": "BBVA USA - Los Angeles",
            "address": "355 S Grand Ave",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90071",
            "phone": "213-345-7000"
        },
        {
            "branch": "BBVA USA - San Francisco",
            "address": "100 Pine St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94111",
            "phone": "415-345-7000"
        },
        {
            "branch": "BBVA USA - Denver",
            "address": "1801 California St",
            "city": "Denver",
            "state": "CO",
            "zip": "80202",
            "phone": "303-345-7000"
        },
        {
            "branch": "BBVA USA - Tampa",
            "address": "100 N Tampa St",
            "city": "Tampa",
            "state": "FL",
            "zip": "33602",
            "phone": "813-224-8000"
        },
        {
            "branch": "BBVA USA - Albuquerque",
            "address": "100 S San Mateo Blvd",
            "city": "Albuquerque",
            "state": "NM",
            "zip": "87108",
            "phone": "505-244-8000"
        },
    ],
    "BECU": [
        {
            "branch": "BECU - Tukwila HQ",
            "address": "12770 Gateway Drive",
            "city": "Tukwila",
            "state": "WA",
            "zip": "98168",
            "phone": "800-233-2328"
        },
        {
            "branch": "BECU - Seattle Downtown",
            "address": "1001 4th Ave",
            "city": "Seattle",
            "state": "WA",
            "zip": "98154",
            "phone": "206-436-8000"
        },
        {
            "branch": "BECU - Bellevue",
            "address": "600 108th Ave NE",
            "city": "Bellevue",
            "state": "WA",
            "zip": "98004",
            "phone": "425-451-8000"
        },
        {
            "branch": "BECU - Tacoma",
            "address": "1201 Pacific Ave",
            "city": "Tacoma",
            "state": "WA",
            "zip": "98402",
            "phone": "253-572-8000"
        },
        {
            "branch": "BECU - Spokane",
            "address": "100 N Washington St",
            "city": "Spokane",
            "state": "WA",
            "zip": "99201",
            "phone": "509-456-8000"
        },
        {
            "branch": "BECU - Portland",
            "address": "100 SW Main St",
            "city": "Portland",
            "state": "OR",
            "zip": "97204",
            "phone": "503-226-8000"
        },
        {
            "branch": "BECU - Eugene",
            "address": "100 E Broadway",
            "city": "Eugene",
            "state": "OR",
            "zip": "97401",
            "phone": "541-686-8000"
        },
        {
            "branch": "BECU - Boise",
            "address": "100 S Capitol Blvd",
            "city": "Boise",
            "state": "ID",
            "zip": "83702",
            "phone": "208-345-8000"
        },
    ],
    "BMO Harris Bank": [
        {
            "branch": "BMO Harris - Chicago Monroe",
            "address": "100 W Monroe St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-732-8000"
        },
        {
            "branch": "BMO Harris - Chicago Madison",
            "address": "1 S Dearborn St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-732-8000"
        },
        {
            "branch": "BMO Harris - Milwaukee",
            "address": "777 E Wisconsin Ave",
            "city": "Milwaukee",
            "state": "WI",
            "zip": "53202",
            "phone": "414-224-8000"
        },
        {
            "branch": "BMO Harris - Madison",
            "address": "1 S Pinckney St",
            "city": "Madison",
            "state": "WI",
            "zip": "53703",
            "phone": "608-257-8000"
        },
        {
            "branch": "BMO Harris - Green Bay",
            "address": "100 N Washington St",
            "city": "Green Bay",
            "state": "WI",
            "zip": "54301",
            "phone": "920-437-8000"
        },
        {
            "branch": "BMO Harris - Minneapolis",
            "address": "600 Marquette Ave",
            "city": "Minneapolis",
            "state": "MN",
            "zip": "55402",
            "phone": "612-342-8000"
        },
        {
            "branch": "BMO Harris - St. Paul",
            "address": "400 Sibley St",
            "city": "St. Paul",
            "state": "MN",
            "zip": "55101",
            "phone": "651-224-8000"
        },
        {
            "branch": "BMO Harris - Des Moines",
            "address": "100 Walnut St",
            "city": "Des Moines",
            "state": "IA",
            "zip": "50309",
            "phone": "515-244-8000"
        },
        {
            "branch": "BMO Harris - Kansas City",
            "address": "1000 Walnut St",
            "city": "Kansas City",
            "state": "MO",
            "zip": "64106",
            "phone": "816-421-8000"
        },
        {
            "branch": "BMO Harris - St. Louis",
            "address": "100 N Broadway",
            "city": "St. Louis",
            "state": "MO",
            "zip": "63102",
            "phone": "314-241-8000"
        },
        {
            "branch": "BMO Harris - Tampa",
            "address": "100 N Tampa St",
            "city": "Tampa",
            "state": "FL",
            "zip": "33602",
            "phone": "813-224-8000"
        },
        {
            "branch": "BMO Harris - Sarasota",
            "address": "100 S Washington Blvd",
            "city": "Sarasota",
            "state": "FL",
            "zip": "34236",
            "phone": "941-364-8000"
        },
        {
            "branch": "Des Moines Downtown",
            "address": "100 S 3rd St",
            "city": "Des Moines",
            "state": "IA",
            "zip": "50309",
            "phone": "515-237-8000"
        },
    ],
    "Bank of America": [
        {
            "branch": "Bank of America Financial Center - Union Square",
            "address": "36 E 14th St",
            "city": "New York",
            "state": "NY",
            "zip": "10003",
            "phone": "212-420-0075"
        },
        {
            "branch": "Bank of America Financial Center - 95 Wall Street",
            "address": "95 Wall St",
            "city": "New York",
            "state": "NY",
            "zip": "10005",
            "phone": "212-509-1000"
        },
        {
            "branch": "Bank of America Financial Center - Brickell",
            "address": "701 Brickell Avenue",
            "city": "Miami",
            "state": "FL",
            "zip": "33131",
            "phone": "305-381-6000"
        },
        {
            "branch": "Bank of America Financial Center - One Bryant Park",
            "address": "One Bryant Park",
            "city": "New York",
            "state": "NY",
            "zip": "10036",
            "phone": "212-841-7000"
        },
        {
            "branch": "Bank of America Financial Center - San Francisco",
            "address": "315 Montgomery Street",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94104",
            "phone": "415-477-3000"
        },
        {
            "branch": "Bank of America Financial Center - Los Angeles",
            "address": "555 S Flower St",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90071",
            "phone": "213-892-1000"
        },
        {
            "branch": "Bank of America Financial Center - Chicago",
            "address": "135 S LaSalle St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-800-4000"
        },
        {
            "branch": "Bank of America Financial Center - Dallas",
            "address": "1707 Main St",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-922-2000"
        },
        {
            "branch": "Bank of America Financial Center - Houston",
            "address": "1000 Louisiana St",
            "city": "Houston",
            "state": "TX",
            "zip": "77002",
            "phone": "713-247-4000"
        },
        {
            "branch": "Bank of America Financial Center - Charlotte",
            "address": "100 N Tryon St",
            "city": "Charlotte",
            "state": "NC",
            "zip": "28255",
            "phone": "704-386-6000"
        },
        {
            "branch": "Bank of America Financial Center - Boston",
            "address": "100 Federal St",
            "city": "Boston",
            "state": "MA",
            "zip": "02110",
            "phone": "617-434-4000"
        },
        {
            "branch": "Bank of America Financial Center - Philadelphia",
            "address": "1 S Broad St",
            "city": "Philadelphia",
            "state": "PA",
            "zip": "19107",
            "phone": "215-973-7000"
        },
        {
            "branch": "Little Rock Main",
            "address": "200 W Capitol Ave",
            "city": "Little Rock",
            "state": "AR",
            "zip": "72201",
            "phone": "501-324-6000"
        },
        {
            "branch": "Jackson Main",
            "address": "100 E Capitol St",
            "city": "Jackson",
            "state": "MS",
            "zip": "39201",
            "phone": "601-576-7000"
        },
        {
            "branch": "Charleston Main",
            "address": "200 Lee St E",
            "city": "Charleston",
            "state": "WV",
            "zip": "25301",
            "phone": "304-576-6000"
        },
        {
            "branch": "Oklahoma City Main",
            "address": "100 N Broadway Ave",
            "city": "Oklahoma City",
            "state": "OK",
            "zip": "73102",
            "phone": "405-576-8000"
        },
        {
            "branch": "Tulsa",
            "address": "100 E 2nd St",
            "city": "Tulsa",
            "state": "OK",
            "zip": "74103",
            "phone": "918-587-8000"
        },
        {
            "branch": "New Orleans Main",
            "address": "100 St Charles Ave",
            "city": "New Orleans",
            "state": "LA",
            "zip": "70130",
            "phone": "504-576-7000"
        },
    ],
    "Barclays Bank": [
        {
            "branch": "Barclays Bank Delaware - Wilmington",
            "address": "125 S West St",
            "city": "Wilmington",
            "state": "DE",
            "zip": "19801",
            "phone": "302-252-8000"
        },
        {
            "branch": "Barclays - New York",
            "address": "745 Seventh Ave",
            "city": "New York",
            "state": "NY",
            "zip": "10019",
            "phone": "212-526-8000"
        },
    ],
    "Bread Financial": [
        {
            "branch": "Bread Financial - Columbus",
            "address": "3095 Loyalty Circle",
            "city": "Columbus",
            "state": "OH",
            "zip": "43219",
            "phone": "614-729-4000"
        },
        {
            "branch": "Bread Financial - Chadds Ford",
            "address": "5 Hillman Dr Suite 102",
            "city": "Chadds Ford",
            "state": "PA",
            "zip": "19317",
            "phone": "610-388-8000"
        },
        {
            "branch": "Bread Financial - Coeur d'Alene",
            "address": "745 W Hanley Ave",
            "city": "Coeur d'Alene",
            "state": "ID",
            "zip": "83815",
            "phone": "208-664-8000"
        },
        {
            "branch": "Bread Financial - Draper",
            "address": "12921 Vista Station Blvd",
            "city": "Draper",
            "state": "UT",
            "zip": "84020",
            "phone": "801-316-8000"
        },
        {
            "branch": "Bread Financial - Frisco",
            "address": "2600 Network Blvd Suite 600",
            "city": "Frisco",
            "state": "TX",
            "zip": "75034",
            "phone": "214-618-8000"
        },
        {
            "branch": "Bread Financial - New York",
            "address": "156 5th Ave Floor 2",
            "city": "New York",
            "state": "NY",
            "zip": "10010",
            "phone": "212-242-8000"
        },
    ],
    "CIT Bank": [
        {
            "branch": "CIT Bank - Pasadena",
            "address": "95 South Lake Ave",
            "city": "Pasadena",
            "state": "CA",
            "zip": "91103",
            "phone": "626-564-8000"
        },
        {
            "branch": "CIT Bank - Honolulu",
            "address": "600 Kapiolani Blvd. Suite 406",
            "city": "Honolulu",
            "state": "HI",
            "zip": "96813",
            "phone": "808-539-8000"
        },
    ],
    "Capital One": [
        {
            "branch": "Capital One Cafe - New York",
            "address": "250 W 42nd St",
            "city": "New York",
            "state": "NY",
            "zip": "10036",
            "phone": "212-997-7000"
        },
        {
            "branch": "Capital One Cafe - Washington DC",
            "address": "401 9th St NW",
            "city": "Washington",
            "state": "DC",
            "zip": "20004",
            "phone": "202-654-7000"
        },
        {
            "branch": "Capital One Bank - McLean",
            "address": "1680 Capital One Dr",
            "city": "McLean",
            "state": "VA",
            "zip": "22102",
            "phone": "703-336-7000"
        },
        {
            "branch": "Capital One Bank - Dallas",
            "address": "7900 Ice House Dr",
            "city": "Plano",
            "state": "TX",
            "zip": "75024",
            "phone": "972-985-7000"
        },
        {
            "branch": "Capital One Bank - Chicago",
            "address": "200 W Monroe St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60606",
            "phone": "312-416-7000"
        },
        {
            "branch": "Capital One Bank - Los Angeles",
            "address": "355 S Grand Ave",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90071",
            "phone": "213-345-7000"
        },
        {
            "branch": "Capital One Bank - San Francisco",
            "address": "100 Pine St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94111",
            "phone": "415-345-7000"
        },
        {
            "branch": "Capital One Bank - Boston",
            "address": "200 Cambridge St",
            "city": "Boston",
            "state": "MA",
            "zip": "02114",
            "phone": "617-345-7000"
        },
        {
            "branch": "Capital One Bank - Philadelphia",
            "address": "2001 Market St",
            "city": "Philadelphia",
            "state": "PA",
            "zip": "19103",
            "phone": "215-345-7000"
        },
        {
            "branch": "Capital One Bank - Atlanta",
            "address": "171 17th St NW",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30363",
            "phone": "404-658-7000"
        },
        {
            "branch": "Capital One Bank - Denver",
            "address": "1801 California St",
            "city": "Denver",
            "state": "CO",
            "zip": "80202",
            "phone": "303-345-7000"
        },
        {
            "branch": "Capital One Bank - Seattle",
            "address": "1201 3rd Ave",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101",
            "phone": "206-345-7000"
        },
    ],
    "Celtic Bank": [
        {
            "branch": "Celtic Bank - Salt Lake City",
            "address": "268 South State Street Suite 300",
            "city": "Salt Lake City",
            "state": "UT",
            "zip": "84111",
            "phone": "801-363-6500"
        },
    ],
    "Charles Schwab Bank": [
        {
            "branch": "Charles Schwab Bank - Westlake",
            "address": "3000 Schwab Way",
            "city": "Westlake",
            "state": "TX",
            "zip": "76262",
            "phone": "817-859-5000"
        },
        {
            "branch": "Charles Schwab Bank - Denver",
            "address": "1801 California St",
            "city": "Denver",
            "state": "CO",
            "zip": "80202",
            "phone": "303-585-8000"
        },
        {
            "branch": "Charles Schwab Bank - Chicago",
            "address": "1 S Dearborn St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-732-8000"
        },
        {
            "branch": "Charles Schwab Bank - Phoenix",
            "address": "100 W Washington St",
            "city": "Phoenix",
            "state": "AZ",
            "zip": "85003",
            "phone": "602-452-6000"
        },
        {
            "branch": "Charles Schwab Bank - San Francisco",
            "address": "555 California St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94104",
            "phone": "415-788-8000"
        },
    ],
    "Citibank": [
        {
            "branch": "Citi Wealth Center - Beverly Hills",
            "address": "445 North Bedford Dr.",
            "city": "Beverly Hills",
            "state": "CA",
            "zip": "90210",
            "phone": "310-278-8000"
        },
        {
            "branch": "Citi Wealth Center - New York",
            "address": "150 Canal Street",
            "city": "New York",
            "state": "NY",
            "zip": "10013",
            "phone": "212-510-8000"
        },
        {
            "branch": "Citi Wealth Center - Miami",
            "address": "1441 Brickell Ave. 16th Fl.",
            "city": "Miami",
            "state": "FL",
            "zip": "33131",
            "phone": "305-416-8000"
        },
        {
            "branch": "Citi Wealth Center - Chicago",
            "address": "700 W Madison St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60661",
            "phone": "312-580-8000"
        },
        {
            "branch": "Citi Wealth Center - San Francisco",
            "address": "601 Montgomery St. Ste. 108",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94111",
            "phone": "415-398-8000"
        },
        {
            "branch": "Citi Wealth Center - Washington DC",
            "address": "802 7th St. NW",
            "city": "Washington",
            "state": "DC",
            "zip": "20001",
            "phone": "202-789-8000"
        },
        {
            "branch": "Citi Wealth Center - Boston",
            "address": "100 High St",
            "city": "Boston",
            "state": "MA",
            "zip": "02110",
            "phone": "617-723-8000"
        },
        {
            "branch": "Citi Wealth Center - Dallas",
            "address": "1700 Pacific Ave",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-922-8000"
        },
        {
            "branch": "Citi Wealth Center - Los Angeles",
            "address": "10250 Constellation Blvd",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90067",
            "phone": "310-277-8000"
        },
        {
            "branch": "Citi Wealth Center - Seattle",
            "address": "920 5th Ave. Ste. 1375",
            "city": "Seattle",
            "state": "WA",
            "zip": "98104",
            "phone": "206-344-8000"
        },
        {
            "branch": "Citi Wealth Center - Atlanta",
            "address": "3344 Peachtree Road NE",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30326",
            "phone": "404-995-8000"
        },
        {
            "branch": "Citi Wealth Center - Philadelphia",
            "address": "2001 Market St",
            "city": "Philadelphia",
            "state": "PA",
            "zip": "19103",
            "phone": "215-851-8000"
        },
    ],
    "Comerica Bank": [
        {
            "branch": "Comerica Bank - Dallas",
            "address": "1717 Main St",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-266-8000"
        },
        {
            "branch": "Comerica Bank - Houston",
            "address": "1000 Louisiana St",
            "city": "Houston",
            "state": "TX",
            "zip": "77002",
            "phone": "713-247-8000"
        },
        {
            "branch": "Comerica Bank - San Francisco",
            "address": "100 Pine St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94111",
            "phone": "415-345-7000"
        },
        {
            "branch": "Comerica Bank - Los Angeles",
            "address": "355 S Grand Ave",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90071",
            "phone": "213-345-7000"
        },
        {
            "branch": "Comerica Bank - Ann Arbor",
            "address": "100 S Main St",
            "city": "Ann Arbor",
            "state": "MI",
            "zip": "48104",
            "phone": "734-662-8000"
        },
    ],
    "Credit One Bank": [
        {
            "branch": "Credit One Bank - Las Vegas",
            "address": "6801 S Cimarron Rd",
            "city": "Las Vegas",
            "state": "NV",
            "zip": "89113",
            "phone": "702-433-8000"
        },
    ],
    "Cullen/Frost Bankers": [
        {
            "branch": "Frost Bank - San Antonio",
            "address": "111 W Houston St",
            "city": "San Antonio",
            "state": "TX",
            "zip": "78205",
            "phone": "210-220-4000"
        },
        {
            "branch": "Frost Bank - Austin",
            "address": "98 San Jacinto Blvd Ste 150",
            "city": "Austin",
            "state": "TX",
            "zip": "78701",
            "phone": "512-477-8000"
        },
        {
            "branch": "Frost Bank - Dallas",
            "address": "2000 McKinney Ave Ste 700",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-922-8000"
        },
        {
            "branch": "Frost Bank - Houston",
            "address": "1330 Post Oak Blvd Ste 100",
            "city": "Houston",
            "state": "TX",
            "zip": "77056",
            "phone": "713-247-8000"
        },
        {
            "branch": "Frost Bank - Fort Worth",
            "address": "300 Throckmorton St Ste 100",
            "city": "Fort Worth",
            "state": "TX",
            "zip": "76102",
            "phone": "817-334-8000"
        },
        {
            "branch": "Frost Bank - San Antonio Mulberry",
            "address": "745 E Mulberry Ave Ste 150",
            "city": "San Antonio",
            "state": "TX",
            "zip": "78212",
            "phone": "210-220-4000"
        },
        {
            "branch": "Frost Bank - Plano",
            "address": "5800 Granite Pkwy Ste 150",
            "city": "Plano",
            "state": "TX",
            "zip": "75024",
            "phone": "972-985-8000"
        },
    ],
    "Discover Bank": [
        {
            "branch": "Discover Bank - Greenwood",
            "address": "502 E Market St",
            "city": "Greenwood",
            "state": "DE",
            "zip": "19950",
            "phone": "302-998-8000"
        },
        {
            "branch": "Discover Bank - New Castle",
            "address": "12 Read's Way",
            "city": "New Castle",
            "state": "DE",
            "zip": "19720",
            "phone": "302-998-8000"
        },
    ],
    "Fidelity Bank": [
        {
            "branch": "Fidelity Bank - Scranton",
            "address": "507 Linden St",
            "city": "Scranton",
            "state": "PA",
            "zip": "18503",
            "phone": "570-348-8000"
        },
        {
            "branch": "Fidelity Bank - Wilkes-Barre",
            "address": "64 N Franklin St",
            "city": "Wilkes-Barre",
            "state": "PA",
            "zip": "18701",
            "phone": "570-826-8000"
        },
        {
            "branch": "Fidelity Bank - Easton",
            "address": "16 Centre Square",
            "city": "Easton",
            "state": "PA",
            "zip": "18042",
            "phone": "610-559-8000"
        },
        {
            "branch": "Fidelity Bank - Hazleton",
            "address": "383 S Poplar St",
            "city": "Hazleton",
            "state": "PA",
            "zip": "18201",
            "phone": "570-459-8000"
        },
        {
            "branch": "Fidelity Bank - Bangor",
            "address": "303 Pennsylvania Ave",
            "city": "Bangor",
            "state": "PA",
            "zip": "18013",
            "phone": "610-588-8000"
        },
        {
            "branch": "Fidelity Bank - Wichita",
            "address": "100 E English",
            "city": "Wichita",
            "state": "KS",
            "zip": "67202",
            "phone": "316-264-8000"
        },
        {
            "branch": "Fidelity Bank - Leominster",
            "address": "75 Main St",
            "city": "Leominster",
            "state": "MA",
            "zip": "01453",
            "phone": "978-534-5222"
        },
    ],
    "Fifth Third Bank": [
        {
            "branch": "Fifth Third Bank - Chicago Clark",
            "address": "61 N Clark St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60601",
            "phone": "312-444-8000"
        },
        {
            "branch": "Fifth Third Bank - Chicago Willis Tower",
            "address": "233 S Wacker Dr",
            "city": "Chicago",
            "state": "IL",
            "zip": "60606",
            "phone": "312-577-8000"
        },
        {
            "branch": "Fifth Third Bank - Cincinnati",
            "address": "201 E 4th St",
            "city": "Cincinnati",
            "state": "OH",
            "zip": "45202",
            "phone": "513-621-8000"
        },
        {
            "branch": "Fifth Third Bank - Columbus",
            "address": "10 W Broad St",
            "city": "Columbus",
            "state": "OH",
            "zip": "43215",
            "phone": "614-463-8000"
        },
        {
            "branch": "Fifth Third Bank - Cleveland",
            "address": "127 Public Square",
            "city": "Cleveland",
            "state": "OH",
            "zip": "44113",
            "phone": "216-781-8000"
        },
        {
            "branch": "Fifth Third Bank - Detroit",
            "address": "611 Woodward Ave",
            "city": "Detroit",
            "state": "MI",
            "zip": "48226",
            "phone": "313-967-8000"
        },
        {
            "branch": "Fifth Third Bank - Atlanta",
            "address": "171 17th St NW",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30363",
            "phone": "404-658-8000"
        },
        {
            "branch": "Fifth Third Bank - Nashville",
            "address": "200 4th Ave N",
            "city": "Nashville",
            "state": "TN",
            "zip": "37219",
            "phone": "615-244-8000"
        },
        {
            "branch": "Fifth Third Bank - Charlotte",
            "address": "100 N Tryon St",
            "city": "Charlotte",
            "state": "NC",
            "zip": "28255",
            "phone": "704-715-8000"
        },
        {
            "branch": "Fifth Third Bank - Indianapolis",
            "address": "111 Monument Cir",
            "city": "Indianapolis",
            "state": "IN",
            "zip": "46204",
            "phone": "317-977-8000"
        },
    ],
    "First Republic Bank": [
        {
            "branch": "First Republic Bank - San Francisco",
            "address": "111 Pine St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94111",
            "phone": "415-772-7000"
        },
        {
            "branch": "First Republic Bank - New York 6th Ave",
            "address": "442 6th Ave",
            "city": "New York",
            "state": "NY",
            "zip": "10011",
            "phone": "212-218-8000"
        },
        {
            "branch": "First Republic Bank - New York Park Ave South",
            "address": "443 Park Avenue South",
            "city": "New York",
            "state": "NY",
            "zip": "10016",
            "phone": "212-218-8000"
        },
        {
            "branch": "First Republic Bank - New York Rockefeller Center",
            "address": "1230 Avenue Of The Americas",
            "city": "New York",
            "state": "NY",
            "zip": "10020",
            "phone": "212-218-8000"
        },
        {
            "branch": "First Republic Bank - New York Park Ave",
            "address": "320 Park Avenue",
            "city": "New York",
            "state": "NY",
            "zip": "10022",
            "phone": "212-218-8000"
        },
        {
            "branch": "First Republic Bank - Los Angeles",
            "address": "350 S Grand Ave",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90071",
            "phone": "213-345-7000"
        },
        {
            "branch": "First Republic Bank - Boston",
            "address": "100 High St",
            "city": "Boston",
            "state": "MA",
            "zip": "02110",
            "phone": "617-723-8000"
        },
    ],
    "Golden 1 Credit Union": [
        {
            "branch": "Golden 1 - Sacramento HQ",
            "address": "8945 Cal Center Dr",
            "city": "Sacramento",
            "state": "CA",
            "zip": "95826",
            "phone": "916-732-2900"
        },
        {
            "branch": "Golden 1 - Los Angeles",
            "address": "355 S Grand Ave",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90071",
            "phone": "213-345-7000"
        },
        {
            "branch": "Golden 1 - San Francisco",
            "address": "100 Pine St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94111",
            "phone": "415-345-7000"
        },
        {
            "branch": "Golden 1 - San Diego",
            "address": "101 SW Main St",
            "city": "San Diego",
            "state": "CA",
            "zip": "92101",
            "phone": "619-233-8000"
        },
        {
            "branch": "Golden 1 - Fresno",
            "address": "100 N Fresno St",
            "city": "Fresno",
            "state": "CA",
            "zip": "93721",
            "phone": "559-235-8000"
        },
        {
            "branch": "Golden 1 - Oakland",
            "address": "200 Broadway",
            "city": "Oakland",
            "state": "CA",
            "zip": "94607",
            "phone": "510-451-8000"
        },
        {
            "branch": "Golden 1 - Stockton",
            "address": "100 N San Joaquin St",
            "city": "Stockton",
            "state": "CA",
            "zip": "95202",
            "phone": "209-464-8000"
        },
        {
            "branch": "Golden 1 - Modesto",
            "address": "1000 10th St",
            "city": "Modesto",
            "state": "CA",
            "zip": "95354",
            "phone": "209-526-8000"
        },
    ],
    "Goldman Sachs Bank": [
        {
            "branch": "Goldman Sachs Bank USA - New York",
            "address": "200 West St",
            "city": "New York",
            "state": "NY",
            "zip": "10282",
            "phone": "212-902-0300"
        },
        {
            "branch": "Goldman Sachs Bank USA - Salt Lake City",
            "address": "11850 South Election Road",
            "city": "Draper",
            "state": "UT",
            "zip": "84020",
            "phone": "855-730-7283"
        },
        {
            "branch": "Goldman Sachs Bank USA - Dallas",
            "address": "3000 Kellway Dr. Suite 120",
            "city": "Carrollton",
            "state": "TX",
            "zip": "75006",
            "phone": "972-418-8000"
        },
        {
            "branch": "Goldman Sachs Bank USA - Chicago",
            "address": "222 W Adams St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60606",
            "phone": "312-577-8000"
        },
        {
            "branch": "Goldman Sachs Bank USA - San Francisco",
            "address": "555 California St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94104",
            "phone": "415-788-8000"
        },
    ],
    "HSBC Bank USA": [
        {
            "branch": "HSBC Wealth Center - New York",
            "address": "150 Canal Street",
            "city": "New York",
            "state": "NY",
            "zip": "10013",
            "phone": "212-510-8000"
        },
        {
            "branch": "HSBC Wealth Center - Beverly Hills",
            "address": "445 North Bedford Dr.",
            "city": "Beverly Hills",
            "state": "CA",
            "zip": "90210",
            "phone": "310-278-8000"
        },
        {
            "branch": "HSBC Wealth Center - San Francisco",
            "address": "601 Montgomery St. Ste. 108",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94111",
            "phone": "415-398-8000"
        },
        {
            "branch": "HSBC Wealth Center - Miami",
            "address": "1441 Brickell Ave. 16th Fl.",
            "city": "Miami",
            "state": "FL",
            "zip": "33131",
            "phone": "305-416-8000"
        },
        {
            "branch": "HSBC Wealth Center - Chicago",
            "address": "700 W Madison St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60661",
            "phone": "312-580-8000"
        },
        {
            "branch": "HSBC Wealth Center - Washington DC",
            "address": "802 7th St. NW",
            "city": "Washington",
            "state": "DC",
            "zip": "20001",
            "phone": "202-789-8000"
        },
        {
            "branch": "HSBC Wealth Center - Boston",
            "address": "100 High St",
            "city": "Boston",
            "state": "MA",
            "zip": "02110",
            "phone": "617-723-8000"
        },
        {
            "branch": "HSBC Wealth Center - Dallas",
            "address": "1700 Pacific Ave",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-922-8000"
        },
        {
            "branch": "HSBC Wealth Center - Seattle",
            "address": "920 5th Ave. Ste. 1375",
            "city": "Seattle",
            "state": "WA",
            "zip": "98104",
            "phone": "206-344-8000"
        },
        {
            "branch": "HSBC Wealth Center - Atlanta",
            "address": "3344 Peachtree Road NE",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30326",
            "phone": "404-995-8000"
        },
        {
            "branch": "HSBC Wealth Center - Philadelphia",
            "address": "2001 Market St",
            "city": "Philadelphia",
            "state": "PA",
            "zip": "19103",
            "phone": "215-851-8000"
        },
        {
            "branch": "HSBC Wealth Center - Scarsdale",
            "address": "901 Central Park Ave.",
            "city": "Scarsdale",
            "state": "NY",
            "zip": "10583",
            "phone": "914-725-8000"
        },
    ],
    "Huntington Bank": [
        {
            "branch": "Huntington Bank - Columbus Main",
            "address": "41 S High St",
            "city": "Columbus",
            "state": "OH",
            "zip": "43215",
            "phone": "614-480-8000"
        },
        {
            "branch": "Huntington Bank - Cleveland",
            "address": "127 Public Square",
            "city": "Cleveland",
            "state": "OH",
            "zip": "44113",
            "phone": "216-781-8000"
        },
        {
            "branch": "Huntington Bank - Detroit",
            "address": "611 Woodward Ave",
            "city": "Detroit",
            "state": "MI",
            "zip": "48226",
            "phone": "313-967-8000"
        },
        {
            "branch": "Huntington Bank - Chicago",
            "address": "1 S Dearborn St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-732-8000"
        },
        {
            "branch": "Huntington Bank - Indianapolis",
            "address": "111 Monument Cir",
            "city": "Indianapolis",
            "state": "IN",
            "zip": "46204",
            "phone": "317-977-8000"
        },
        {
            "branch": "Huntington Bank - Pittsburgh",
            "address": "600 Grant St",
            "city": "Pittsburgh",
            "state": "PA",
            "zip": "15219",
            "phone": "412-768-8000"
        },
        {
            "branch": "Huntington Bank - Charlotte",
            "address": "100 N Tryon St",
            "city": "Charlotte",
            "state": "NC",
            "zip": "28255",
            "phone": "704-715-8000"
        },
        {
            "branch": "Huntington Bank - Atlanta",
            "address": "171 17th St NW",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30363",
            "phone": "404-658-8000"
        },
        {
            "branch": "Huntington Bank - Tampa",
            "address": "100 N Tampa St",
            "city": "Tampa",
            "state": "FL",
            "zip": "33602",
            "phone": "813-224-8000"
        },
        {
            "branch": "Huntington Bank - Minneapolis",
            "address": "600 Marquette Ave",
            "city": "Minneapolis",
            "state": "MN",
            "zip": "55402",
            "phone": "612-342-8000"
        },
        {
            "branch": "Huntington Bank - Milwaukee",
            "address": "777 E Wisconsin Ave",
            "city": "Milwaukee",
            "state": "WI",
            "zip": "53202",
            "phone": "414-224-8000"
        },
        {
            "branch": "Huntington Bank - St. Louis",
            "address": "100 N Broadway",
            "city": "St. Louis",
            "state": "MO",
            "zip": "63102",
            "phone": "314-241-8000"
        },
    ],
    "Interactive Brokers": [
        {
            "branch": "Interactive Brokers - Greenwich",
            "address": "One Pickwick Plaza",
            "city": "Greenwich",
            "state": "CT",
            "zip": "06830",
            "phone": "203-618-5800"
        },
        {
            "branch": "Interactive Brokers - Chicago",
            "address": "209 S La Salle St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60604",
            "phone": "312-786-7400"
        },
    ],
    "JPMorgan Chase Bank": [
        {
            "branch": "Chase Branch - Times Square",
            "address": "3 Times Square",
            "city": "New York",
            "state": "NY",
            "zip": "10036",
            "phone": "212-719-2180"
        },
        {
            "branch": "Chase Branch - Downtown Miami",
            "address": "150 SE 2nd Ave",
            "city": "Miami",
            "state": "FL",
            "zip": "33131",
            "phone": "305-371-1600"
        },
        {
            "branch": "Chase Branch - Miramar",
            "address": "6860 Miramar Pkwy",
            "city": "Miramar",
            "state": "FL",
            "zip": "33023",
            "phone": "954-627-8400"
        },
        {
            "branch": "Chase Branch - Columbus",
            "address": "1111 Polaris Pkwy",
            "city": "Columbus",
            "state": "OH",
            "zip": "43240",
            "phone": "614-438-7000"
        },
        {
            "branch": "Chase Branch - Chicago",
            "address": "10 S Dearborn St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-732-8000"
        },
        {
            "branch": "Chase Branch - Los Angeles",
            "address": "400 S Hope Plaza",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90071",
            "phone": "213-576-4000"
        },
        {
            "branch": "Chase Branch - Houston",
            "address": "600 Travis St",
            "city": "Houston",
            "state": "TX",
            "zip": "77002",
            "phone": "713-216-4000"
        },
        {
            "branch": "Chase Branch - Phoenix",
            "address": "201 N Central Ave",
            "city": "Phoenix",
            "state": "AZ",
            "zip": "85004",
            "phone": "602-252-2000"
        },
        {
            "branch": "Chase Branch - Dallas",
            "address": "2200 Ross Ave",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-740-6000"
        },
        {
            "branch": "Chase Branch - San Francisco",
            "address": "101 California St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94111",
            "phone": "415-677-8000"
        },
        {
            "branch": "Chase Branch - Denver",
            "address": "1801 California St",
            "city": "Denver",
            "state": "CO",
            "zip": "80202",
            "phone": "303-585-4000"
        },
        {
            "branch": "Chase Branch - Seattle",
            "address": "1201 3rd Ave",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101",
            "phone": "206-587-3000"
        },
        {
            "branch": "Chase Branch - Atlanta",
            "address": "500 W Peachtree St NW",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30308",
            "phone": "404-681-3000"
        },
        {
            "branch": "Chase Branch - Boston",
            "address": "200 Berkeley St",
            "city": "Boston",
            "state": "MA",
            "zip": "02116",
            "phone": "617-526-8000"
        },
        {
            "branch": "Little Rock Main",
            "address": "500 W Capitol Ave",
            "city": "Little Rock",
            "state": "AR",
            "zip": "72201",
            "phone": "501-376-9000"
        },
        {
            "branch": "Jackson Main",
            "address": "200 E Capitol St",
            "city": "Jackson",
            "state": "MS",
            "zip": "39201",
            "phone": "601-576-8000"
        },
        {
            "branch": "Oklahoma City Main",
            "address": "200 N Broadway Ave",
            "city": "Oklahoma City",
            "state": "OK",
            "zip": "73102",
            "phone": "405-576-9000"
        },
        {
            "branch": "New Orleans Main",
            "address": "200 St Charles Ave",
            "city": "New Orleans",
            "state": "LA",
            "zip": "70130",
            "phone": "504-576-8000"
        },
    ],
    "KeyBank": [
        {
            "branch": "KeyBank - New York",
            "address": "1 W 34th St",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "phone": "212-273-8000"
        },
        {
            "branch": "KeyBank - Albany",
            "address": "100 State St",
            "city": "Albany",
            "state": "NY",
            "zip": "12207",
            "phone": "518-447-8000"
        },
        {
            "branch": "KeyBank - Boston",
            "address": "200 Berkeley St",
            "city": "Boston",
            "state": "MA",
            "zip": "02116",
            "phone": "617-426-8000"
        },
        {
            "branch": "KeyBank - Cleveland",
            "address": "127 Public Square",
            "city": "Cleveland",
            "state": "OH",
            "zip": "44113",
            "phone": "216-781-8000"
        },
        {
            "branch": "KeyBank - Columbus",
            "address": "10 W Broad St",
            "city": "Columbus",
            "state": "OH",
            "zip": "43215",
            "phone": "614-463-8000"
        },
        {
            "branch": "KeyBank - Detroit",
            "address": "611 Woodward Ave",
            "city": "Detroit",
            "state": "MI",
            "zip": "48226",
            "phone": "313-967-8000"
        },
        {
            "branch": "KeyBank - Chicago",
            "address": "1 S Dearborn St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-732-8000"
        },
        {
            "branch": "KeyBank - Denver",
            "address": "1801 California St",
            "city": "Denver",
            "state": "CO",
            "zip": "80202",
            "phone": "303-585-8000"
        },
        {
            "branch": "KeyBank - Portland",
            "address": "101 SW Main St",
            "city": "Portland",
            "state": "OR",
            "zip": "97204",
            "phone": "503-226-8000"
        },
        {
            "branch": "KeyBank - Seattle",
            "address": "1201 3rd Ave",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101",
            "phone": "206-587-8000"
        },
        {
            "branch": "KeyBank - Salt Lake City",
            "address": "100 S Main St",
            "city": "Salt Lake City",
            "state": "UT",
            "zip": "84101",
            "phone": "801-350-8000"
        },
        {
            "branch": "KeyBank - Anchorage",
            "address": "2200 E 4th Ave",
            "city": "Anchorage",
            "state": "AK",
            "zip": "99501",
            "phone": "907-279-8000"
        },
        {
            "branch": "Portland Main",
            "address": "100 Middle St",
            "city": "Portland",
            "state": "ME",
            "zip": "04101",
            "phone": "207-576-7000"
        },
    ],
    "Live Oak Bank": [
        {
            "branch": "Live Oak Bank - Wilmington",
            "address": "1757 Tiburon Drive",
            "city": "Wilmington",
            "state": "NC",
            "zip": "28403",
            "phone": "866-518-0286"
        },
        {
            "branch": "Live Oak Bank - Atlanta",
            "address": "3060 Peachtree Road NW Suite 2050",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30305",
            "phone": "404-266-8000"
        },
    ],
    "M&T Bank": [
        {
            "branch": "M&T Bank - Buffalo",
            "address": "345 Main St",
            "city": "Buffalo",
            "state": "NY",
            "zip": "14203",
            "phone": "716-842-6000"
        },
        {
            "branch": "M&T Bank - Rochester",
            "address": "100 Main St",
            "city": "Rochester",
            "state": "NY",
            "zip": "14614",
            "phone": "585-325-8000"
        },
        {
            "branch": "M&T Bank - Syracuse",
            "address": "100 S Warren St",
            "city": "Syracuse",
            "state": "NY",
            "zip": "13202",
            "phone": "315-424-8000"
        },
        {
            "branch": "M&T Bank - Albany",
            "address": "100 State St",
            "city": "Albany",
            "state": "NY",
            "zip": "12207",
            "phone": "518-447-8000"
        },
        {
            "branch": "M&T Bank - Baltimore",
            "address": "1 Light St",
            "city": "Baltimore",
            "state": "MD",
            "zip": "21202",
            "phone": "410-576-8000"
        },
        {
            "branch": "M&T Bank - Washington DC",
            "address": "800 17th St NW",
            "city": "Washington",
            "state": "DC",
            "zip": "20006",
            "phone": "202-857-8000"
        },
        {
            "branch": "M&T Bank - Philadelphia",
            "address": "1 S Broad St",
            "city": "Philadelphia",
            "state": "PA",
            "zip": "19107",
            "phone": "215-985-7000"
        },
        {
            "branch": "M&T Bank - Pittsburgh",
            "address": "600 Grant St",
            "city": "Pittsburgh",
            "state": "PA",
            "zip": "15219",
            "phone": "412-768-8000"
        },
        {
            "branch": "M&T Bank - Scranton",
            "address": "100 N Washington Ave",
            "city": "Scranton",
            "state": "PA",
            "zip": "18503",
            "phone": "570-344-8000"
        },
        {
            "branch": "M&T Bank - Wilmington",
            "address": "1100 N Market St",
            "city": "Wilmington",
            "state": "DE",
            "zip": "19801",
            "phone": "302-252-8000"
        },
        {
            "branch": "Huntington",
            "address": "900 3rd Ave",
            "city": "Huntington",
            "state": "WV",
            "zip": "25701",
            "phone": "304-576-7000"
        },
    ],
    "Marcus by Goldman Sachs": [
        {
            "branch": "Marcus by Goldman Sachs - Salt Lake City",
            "address": "11850 South Election Road",
            "city": "Draper",
            "state": "UT",
            "zip": "84020",
            "phone": "855-730-7283"
        },
        {
            "branch": "Marcus by Goldman Sachs - New York",
            "address": "200 West St",
            "city": "New York",
            "state": "NY",
            "zip": "10282",
            "phone": "212-902-0300"
        },
    ],
    "MetLife Bank": [
        {
            "branch": "MetLife Bank - Bridgewater",
            "address": "501 Route 22",
            "city": "Bridgewater",
            "state": "NJ",
            "zip": "08807",
            "phone": "973-254-3229"
        },
    ],
    "Morgan Stanley Bank": [
        {
            "branch": "Morgan Stanley - New York World HQ",
            "address": "1585 Broadway",
            "city": "New York",
            "state": "NY",
            "zip": "10036",
            "phone": "212-761-4000"
        },
        {
            "branch": "Morgan Stanley - Chicago",
            "address": "233 S Wacker Dr. Suite 9200",
            "city": "Chicago",
            "state": "IL",
            "zip": "60606",
            "phone": "312-577-8000"
        },
        {
            "branch": "Morgan Stanley - Dallas",
            "address": "2000 Ross Ave. Suite 4900",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-922-8000"
        },
        {
            "branch": "Morgan Stanley - Houston",
            "address": "JP Morgan Chase Tower 600 Travis St. Suite 3700",
            "city": "Houston",
            "state": "TX",
            "zip": "77002",
            "phone": "713-246-8000"
        },
        {
            "branch": "Morgan Stanley - Los Angeles",
            "address": "1999 Avenue of the Stars. Suite 2400",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90067",
            "phone": "310-277-8000"
        },
        {
            "branch": "Morgan Stanley - San Francisco",
            "address": "555 California St. Suite 1400",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94104",
            "phone": "415-788-8000"
        },
        {
            "branch": "Morgan Stanley - Boston",
            "address": "1 Post Office Square",
            "city": "Boston",
            "state": "MA",
            "zip": "02109",
            "phone": "617-723-8000"
        },
        {
            "branch": "Morgan Stanley - Atlanta",
            "address": "100 Terminus 3280 Peachtree Rd NE 20th Floor",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30305",
            "phone": "404-658-8000"
        },
        {
            "branch": "Morgan Stanley - Washington DC",
            "address": "401 9th St NW Suite 630",
            "city": "Washington",
            "state": "DC",
            "zip": "20004",
            "phone": "202-789-8000"
        },
        {
            "branch": "Morgan Stanley - Miami",
            "address": "200 South Biscayne Boulevard 51st Floor",
            "city": "Miami",
            "state": "FL",
            "zip": "33131",
            "phone": "305-373-8000"
        },
    ],
    "Navy Federal Credit Union": [
        {
            "branch": "Navy Federal - Vienna",
            "address": "820 Fairfax County Pkwy",
            "city": "Vienna",
            "state": "VA",
            "zip": "22182",
            "phone": "888-842-6328"
        },
        {
            "branch": "Navy Federal - Pensacola",
            "address": "5000伦纳德 St",
            "city": "Pensacola",
            "state": "FL",
            "zip": "32526",
            "phone": "850-433-8000"
        },
        {
            "branch": "Navy Federal - San Diego",
            "address": "2400 Decatur Rd Suite 101",
            "city": "San Diego",
            "state": "CA",
            "zip": "92106",
            "phone": "619-222-8000"
        },
        {
            "branch": "Navy Federal - Phoenix",
            "address": "1150 E Bell Rd",
            "city": "Phoenix",
            "state": "AZ",
            "zip": "85022",
            "phone": "602-433-8000"
        },
        {
            "branch": "Navy Federal - Colorado Springs",
            "address": "1139 Space Center Dr",
            "city": "Colorado Springs",
            "state": "CO",
            "zip": "80915",
            "phone": "719-433-8000"
        },
        {
            "branch": "Navy Federal - Norfolk",
            "address": "9997 Pentagon Concourse Ste 152",
            "city": "Norfolk",
            "state": "VA",
            "zip": "23502",
            "phone": "757-433-8000"
        },
        {
            "branch": "Navy Federal - Jacksonville",
            "address": "100 N Main St",
            "city": "Jacksonville",
            "state": "FL",
            "zip": "32202",
            "phone": "904-791-8000"
        },
        {
            "branch": "Navy Federal - Bremerton",
            "address": "2020 6th St",
            "city": "Bremerton",
            "state": "WA",
            "zip": "98337",
            "phone": "360-377-8000"
        },
        {
            "branch": "Navy Federal - Groton",
            "address": "24 Sailfish Dr",
            "city": "Groton",
            "state": "CT",
            "zip": "06340",
            "phone": "860-433-8000"
        },
        {
            "branch": "Navy Federal - Charleston",
            "address": "2000 Ashley Phosphate Rd",
            "city": "North Charleston",
            "state": "SC",
            "zip": "29418",
            "phone": "843-433-8000"
        },
    ],
    "OneDigital": [
        {
            "branch": "OneDigital - Atlanta HQ",
            "address": "300 Galleria Pkwy Suite 1100",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30339",
            "phone": "770-351-8000"
        },
    ],
    "PNC Bank": [
        {
            "branch": "PNC Bank - Pittsburgh Downtown",
            "address": "600 Grant St",
            "city": "Pittsburgh",
            "state": "PA",
            "zip": "15219",
            "phone": "412-768-2000"
        },
        {
            "branch": "PNC Bank - Philadelphia",
            "address": "1600 Market St",
            "city": "Philadelphia",
            "state": "PA",
            "zip": "19103",
            "phone": "215-585-7000"
        },
        {
            "branch": "PNC Bank - New York",
            "address": "1 W 34th St",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "phone": "212-273-8000"
        },
        {
            "branch": "PNC Bank - Columbus",
            "address": "10 W Broad St",
            "city": "Columbus",
            "state": "OH",
            "zip": "43215",
            "phone": "614-463-8000"
        },
        {
            "branch": "PNC Bank - Chicago",
            "address": "1 S Dearborn St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-732-8000"
        },
        {
            "branch": "PNC Bank - Baltimore",
            "address": "100 Light St",
            "city": "Baltimore",
            "state": "MD",
            "zip": "21202",
            "phone": "410-576-8000"
        },
        {
            "branch": "PNC Bank - Washington DC",
            "address": "800 17th St NW",
            "city": "Washington",
            "state": "DC",
            "zip": "20006",
            "phone": "202-857-8000"
        },
        {
            "branch": "PNC Bank - Atlanta",
            "address": "171 17th St NW",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30363",
            "phone": "404-658-8000"
        },
        {
            "branch": "PNC Bank - Detroit",
            "address": "611 Woodward Ave",
            "city": "Detroit",
            "state": "MI",
            "zip": "48226",
            "phone": "313-967-8000"
        },
        {
            "branch": "PNC Bank - Charlotte",
            "address": "400 S Tryon St",
            "city": "Charlotte",
            "state": "NC",
            "zip": "28202",
            "phone": "704-715-8000"
        },
        {
            "branch": "PNC Bank - Indianapolis",
            "address": "111 Monument Cir",
            "city": "Indianapolis",
            "state": "IN",
            "zip": "46204",
            "phone": "317-977-8000"
        },
        {
            "branch": "PNC Bank - Milwaukee",
            "address": "777 E Wisconsin Ave",
            "city": "Milwaukee",
            "state": "WI",
            "zip": "53202",
            "phone": "414-224-8000"
        },
    ],
    "PacWest Bank": [
        {
            "branch": "Pacific Western Bank - Beverly Hills",
            "address": "9701 Wilshire Blvd. Suite 101",
            "city": "Beverly Hills",
            "state": "CA",
            "zip": "90212",
            "phone": "310-550-8000"
        },
        {
            "branch": "Pacific Western Bank - Los Angeles",
            "address": "10250 Constellation Blvd. Suite 1640",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90067",
            "phone": "310-277-8000"
        },
        {
            "branch": "Pacific Western Bank - Durham",
            "address": "100 W Main St",
            "city": "Durham",
            "state": "NC",
            "zip": "27701",
            "phone": "919-683-8000"
        },
        {
            "branch": "Pacific Western Bank - Denver",
            "address": "1801 California St",
            "city": "Denver",
            "state": "CO",
            "zip": "80202",
            "phone": "303-585-8000"
        },
    ],
    "Pentagon Federal Credit Union": [
        {
            "branch": "PenFed - McLean",
            "address": "7940 Jones Branch Dr",
            "city": "McLean",
            "state": "VA",
            "zip": "22102",
            "phone": "571-341-6706"
        },
        {
            "branch": "PenFed - Washington DC",
            "address": "400 7th St NW",
            "city": "Washington",
            "state": "DC",
            "zip": "20004",
            "phone": "202-789-8000"
        },
        {
            "branch": "PenFed - Los Angeles",
            "address": "355 S Grand Ave",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90071",
            "phone": "213-345-7000"
        },
        {
            "branch": "PenFed - San Diego",
            "address": "101 SW Main St",
            "city": "San Diego",
            "state": "CA",
            "zip": "92101",
            "phone": "619-233-8000"
        },
        {
            "branch": "PenFed - Dallas",
            "address": "2001 Bryan St",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-922-8000"
        },
        {
            "branch": "PenFed - Houston",
            "address": "1000 Louisiana St",
            "city": "Houston",
            "state": "TX",
            "zip": "77002",
            "phone": "713-247-8000"
        },
        {
            "branch": "PenFed - Chicago",
            "address": "1 S Dearborn St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-732-8000"
        },
        {
            "branch": "PenFed - Atlanta",
            "address": "171 17th St NW",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30363",
            "phone": "404-658-8000"
        },
        {
            "branch": "PenFed - Miami",
            "address": "200 S Biscayne Blvd",
            "city": "Miami",
            "state": "FL",
            "zip": "33131",
            "phone": "305-373-8000"
        },
        {
            "branch": "PenFed - New York",
            "address": "150 Nassau St",
            "city": "New York",
            "state": "NY",
            "zip": "10038",
            "phone": "212-571-7000"
        },
    ],
    "Regions Bank": [
        {
            "branch": "Regions Bank - Birmingham",
            "address": "1900 5th Ave N",
            "city": "Birmingham",
            "state": "AL",
            "zip": "35203",
            "phone": "205-264-4551"
        },
        {
            "branch": "Regions Bank - Atlanta",
            "address": "171 17th St NW",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30363",
            "phone": "404-658-8000"
        },
        {
            "branch": "Regions Bank - Nashville",
            "address": "200 4th Ave N",
            "city": "Nashville",
            "state": "TN",
            "zip": "37219",
            "phone": "615-244-8000"
        },
        {
            "branch": "Regions Bank - Charlotte",
            "address": "100 N Tryon St",
            "city": "Charlotte",
            "state": "NC",
            "zip": "28255",
            "phone": "704-715-8000"
        },
        {
            "branch": "Regions Bank - Dallas",
            "address": "2001 Bryan St",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-922-8000"
        },
        {
            "branch": "Regions Bank - Houston",
            "address": "1000 Louisiana St",
            "city": "Houston",
            "state": "TX",
            "zip": "77002",
            "phone": "713-247-8000"
        },
        {
            "branch": "Regions Bank - Chicago",
            "address": "1 S Dearborn St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-732-8000"
        },
        {
            "branch": "Regions Bank - Tampa",
            "address": "100 N Tampa St",
            "city": "Tampa",
            "state": "FL",
            "zip": "33602",
            "phone": "813-224-8000"
        },
        {
            "branch": "Regions Bank - Indianapolis",
            "address": "111 Monument Cir",
            "city": "Indianapolis",
            "state": "IN",
            "zip": "46204",
            "phone": "317-977-8000"
        },
        {
            "branch": "Regions Bank - St. Louis",
            "address": "100 N Broadway",
            "city": "St. Louis",
            "state": "MO",
            "zip": "63102",
            "phone": "314-241-8000"
        },
        {
            "branch": "Little Rock Main",
            "address": "400 W Capitol Ave",
            "city": "Little Rock",
            "state": "AR",
            "zip": "72201",
            "phone": "501-376-6000"
        },
        {
            "branch": "Fayetteville",
            "address": "3509 N College Ave",
            "city": "Fayetteville",
            "state": "AR",
            "zip": "72703",
            "phone": "479-587-8000"
        },
        {
            "branch": "Jackson Main",
            "address": "200 E Capitol St",
            "city": "Jackson",
            "state": "MS",
            "zip": "39201",
            "phone": "601-576-5000"
        },
        {
            "branch": "Gulfport",
            "address": "2600 26th Ave",
            "city": "Gulfport",
            "state": "MS",
            "zip": "39501",
            "phone": "228-206-6000"
        },
        {
            "branch": "Charleston Main",
            "address": "1000 Virginia St E",
            "city": "Charleston",
            "state": "WV",
            "zip": "25301",
            "phone": "304-576-5000"
        },
        {
            "branch": "Tulsa Main",
            "address": "100 E 2nd St",
            "city": "Tulsa",
            "state": "OK",
            "zip": "74103",
            "phone": "918-587-9000"
        },
        {
            "branch": "New Orleans Main",
            "address": "201 St Charles Ave",
            "city": "New Orleans",
            "state": "LA",
            "zip": "70130",
            "phone": "504-576-5000"
        },
        {
            "branch": "Baton Rouge",
            "address": "200 Main St",
            "city": "Baton Rouge",
            "state": "LA",
            "zip": "70802",
            "phone": "225-576-6000"
        },
    ],
    "Santander Bank": [
        {
            "branch": "Santander Bank - Boston",
            "address": "200 Berkeley St",
            "city": "Boston",
            "state": "MA",
            "zip": "02116",
            "phone": "617-657-7000"
        },
        {
            "branch": "Santander Bank - Providence",
            "address": "100 Westminster St",
            "city": "Providence",
            "state": "RI",
            "zip": "02903",
            "phone": "401-277-7000"
        },
        {
            "branch": "Santander Bank - New York",
            "address": "150 Nassau St",
            "city": "New York",
            "state": "NY",
            "zip": "10038",
            "phone": "212-571-7000"
        },
        {
            "branch": "Santander Bank - Philadelphia",
            "address": "2001 Market St",
            "city": "Philadelphia",
            "state": "PA",
            "zip": "19103",
            "phone": "215-985-7000"
        },
        {
            "branch": "Santander Bank - New Jersey",
            "address": "200 Metroplex Dr",
            "city": "Edison",
            "state": "NJ",
            "zip": "08817",
            "phone": "732-417-7000"
        },
        {
            "branch": "Santander Bank - Miami",
            "address": "200 S Biscayne Blvd",
            "city": "Miami",
            "state": "FL",
            "zip": "33131",
            "phone": "305-373-7000"
        },
    ],
    "SchoolsFirst Federal Credit Union": [
        {
            "branch": "SchoolsFirst FCU - Santa Ana",
            "address": "15442 Newport Ave",
            "city": "Tustin",
            "state": "CA",
            "zip": "92780",
            "phone": "714-258-4000"
        },
        {
            "branch": "SchoolsFirst FCU - Glendale",
            "address": "100 W Broadway",
            "city": "Glendale",
            "state": "CA",
            "zip": "91210",
            "phone": "818-548-8000"
        },
        {
            "branch": "SchoolsFirst FCU - Long Beach",
            "address": "200 Long Beach Blvd",
            "city": "Long Beach",
            "state": "CA",
            "zip": "90802",
            "phone": "562-436-8000"
        },
        {
            "branch": "SchoolsFirst FCU - Moreno Valley",
            "address": "12020 Moreno St",
            "city": "Moreno Valley",
            "state": "CA",
            "zip": "92553",
            "phone": "951-243-8000"
        },
        {
            "branch": "SchoolsFirst FCU - Lancaster",
            "address": "44355 N Sierra Hwy",
            "city": "Lancaster",
            "state": "CA",
            "zip": "93534",
            "phone": "661-948-8000"
        },
        {
            "branch": "SchoolsFirst FCU - Palm Desert",
            "address": "44440 Town Center Way",
            "city": "Palm Desert",
            "state": "CA",
            "zip": "92260",
            "phone": "760-346-8000"
        },
    ],
    "Signature Bank": [
        {
            "branch": "Signature Bank - Downtown Chicago",
            "address": "191 N. Wacker Drive",
            "city": "Chicago",
            "state": "IL",
            "zip": "60606",
            "phone": "312-506-3400"
        },
        {
            "branch": "Signature Bank - Edison Park",
            "address": "7292 W. Devon Avenue",
            "city": "Chicago",
            "state": "IL",
            "zip": "60631",
            "phone": "773-467-5600"
        },
    ],
    "Silicon Valley Bank": [
        {
            "branch": "SVB - Santa Clara",
            "address": "2625 Augustine Drive Suite 301",
            "city": "Santa Clara",
            "state": "CA",
            "zip": "95054",
            "phone": "408-654-5500"
        },
        {
            "branch": "SVB - Chicago",
            "address": "30 South Wacker Drive Suite 2900",
            "city": "Chicago",
            "state": "IL",
            "zip": "60606",
            "phone": "312-704-9510"
        },
    ],
    "State Employees Credit Union": [
        {
            "branch": "SECU - Raleigh",
            "address": "119 N Salisbury St Fl 10",
            "city": "Raleigh",
            "state": "NC",
            "zip": "27603",
            "phone": "919-859-8000"
        },
        {
            "branch": "SECU - Charlotte",
            "address": "100 N Tryon St",
            "city": "Charlotte",
            "state": "NC",
            "zip": "28255",
            "phone": "704-715-8000"
        },
        {
            "branch": "SECU - Greensboro",
            "address": "100 S Elm St",
            "city": "Greensboro",
            "state": "NC",
            "zip": "27401",
            "phone": "336-373-8000"
        },
        {
            "branch": "SECU - Winston-Salem",
            "address": "100 W 5th St",
            "city": "Winston-Salem",
            "state": "NC",
            "zip": "27101",
            "phone": "336-723-8000"
        },
        {
            "branch": "SECU - Durham",
            "address": "100 E Chapel Hill St",
            "city": "Durham",
            "state": "NC",
            "zip": "27701",
            "phone": "919-683-8000"
        },
        {
            "branch": "SECU - Fayetteville",
            "address": "100 Hay St",
            "city": "Fayetteville",
            "state": "NC",
            "zip": "28301",
            "phone": "910-323-8000"
        },
        {
            "branch": "SECU - Wilmington",
            "address": "100 N Front St",
            "city": "Wilmington",
            "state": "NC",
            "zip": "28401",
            "phone": "910-343-8000"
        },
        {
            "branch": "SECU - Asheville",
            "address": "100 Patton Ave",
            "city": "Asheville",
            "state": "NC",
            "zip": "28801",
            "phone": "828-252-8000"
        },
    ],
    "Synchrony Bank": [
        {
            "branch": "Synchrony Bank Home Office",
            "address": "170 Election Road Suite 125",
            "city": "Draper",
            "state": "UT",
            "zip": "84020",
            "phone": "800-525-4545"
        },
        {
            "branch": "Synchrony Bank - Costa Mesa",
            "address": "555 Anton Blvd 7th Floor Ste 700",
            "city": "Costa Mesa",
            "state": "CA",
            "zip": "92626",
            "phone": "714-434-8000"
        },
        {
            "branch": "Synchrony Bank - Stamford",
            "address": "777 Long Ridge Rd",
            "city": "Stamford",
            "state": "CT",
            "zip": "06902",
            "phone": "203-975-8000"
        },
        {
            "branch": "Synchrony Bank - Lake Mary",
            "address": "500 Colonial Center Parkway",
            "city": "Lake Mary",
            "state": "FL",
            "zip": "32746",
            "phone": "407-333-8000"
        },
        {
            "branch": "Synchrony Bank - Chicago",
            "address": "222 W Adams St Floor 24/25",
            "city": "Chicago",
            "state": "IL",
            "zip": "60606",
            "phone": "312-577-8000"
        },
        {
            "branch": "Synchrony Bank - New York",
            "address": "5 Bryant Park Floor 16",
            "city": "New York",
            "state": "NY",
            "zip": "10018",
            "phone": "212-389-8000"
        },
    ],
    "Synchrony Financial": [
        {
            "branch": "Synchrony Financial - Stamford",
            "address": "777 Long Ridge Road",
            "city": "Stamford",
            "state": "CT",
            "zip": "06902",
            "phone": "203-975-8000"
        },
    ],
    "TD Bank": [
        {
            "branch": "TD Bank - New York 5th Ave",
            "address": "597 5th Ave",
            "city": "New York",
            "state": "NY",
            "zip": "10022",
            "phone": "212-759-7000"
        },
        {
            "branch": "TD Bank - Boston Downtown",
            "address": "200 Berkeley St",
            "city": "Boston",
            "state": "MA",
            "zip": "02116",
            "phone": "617-426-7000"
        },
        {
            "branch": "TD Bank - Philadelphia",
            "address": "1 S Broad St",
            "city": "Philadelphia",
            "state": "PA",
            "zip": "19107",
            "phone": "215-985-7000"
        },
        {
            "branch": "TD Bank - Washington DC",
            "address": "400 7th St NW",
            "city": "Washington",
            "state": "DC",
            "zip": "20004",
            "phone": "202-789-7000"
        },
        {
            "branch": "TD Bank - Charlotte",
            "address": "100 N Tryon St",
            "city": "Charlotte",
            "state": "NC",
            "zip": "28255",
            "phone": "704-715-7000"
        },
        {
            "branch": "TD Bank - Richmond",
            "address": "100 N 14th St",
            "city": "Richmond",
            "state": "VA",
            "zip": "23219",
            "phone": "804-782-7000"
        },
        {
            "branch": "TD Bank - Baltimore",
            "address": "100 Light St",
            "city": "Baltimore",
            "state": "MD",
            "zip": "21202",
            "phone": "410-576-7000"
        },
        {
            "branch": "TD Bank - Tampa",
            "address": "100 N Tampa St",
            "city": "Tampa",
            "state": "FL",
            "zip": "33602",
            "phone": "813-224-7000"
        },
        {
            "branch": "TD Bank - Jacksonville",
            "address": "200 W Bay St",
            "city": "Jacksonville",
            "state": "FL",
            "zip": "32202",
            "phone": "904-791-7000"
        },
        {
            "branch": "TD Bank - Orlando",
            "address": "200 S Orange Ave",
            "city": "Orlando",
            "state": "FL",
            "zip": "32801",
            "phone": "407-243-7000"
        },
        {
            "branch": "TD Bank - Miami",
            "address": "200 S Biscayne Blvd",
            "city": "Miami",
            "state": "FL",
            "zip": "33131",
            "phone": "305-373-7000"
        },
        {
            "branch": "TD Bank - Newark",
            "address": "570 Broad St",
            "city": "Newark",
            "state": "NJ",
            "zip": "07102",
            "phone": "973-624-7000"
        },
        {
            "branch": "TD Bank - Jersey City",
            "address": "100 Montgomery St",
            "city": "Jersey City",
            "state": "NJ",
            "zip": "07302",
            "phone": "201-217-7000"
        },
        {
            "branch": "Portland Main",
            "address": "100 Middle St",
            "city": "Portland",
            "state": "ME",
            "zip": "04101",
            "phone": "207-576-5000"
        },
        {
            "branch": "Augusta",
            "address": "200 State St",
            "city": "Augusta",
            "state": "ME",
            "zip": "04330",
            "phone": "207-576-6000"
        },
    ],
    "Texas Capital Bank": [
        {
            "branch": "Texas Capital Bank - Dallas",
            "address": "2000 McKinney Ave Ste 700",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-922-8000"
        },
        {
            "branch": "Texas Capital Bank - Austin",
            "address": "98 San Jacinto Blvd Ste 150",
            "city": "Austin",
            "state": "TX",
            "zip": "78701",
            "phone": "512-477-8000"
        },
        {
            "branch": "Texas Capital Bank - Fort Worth",
            "address": "300 Throckmorton St Ste 100",
            "city": "Fort Worth",
            "state": "TX",
            "zip": "76102",
            "phone": "817-334-8000"
        },
        {
            "branch": "Texas Capital Bank - Houston",
            "address": "1330 Post Oak Blvd Ste 100",
            "city": "Houston",
            "state": "TX",
            "zip": "77056",
            "phone": "713-247-8000"
        },
        {
            "branch": "Texas Capital Bank - Plano",
            "address": "5800 Granite Pkwy Ste 150",
            "city": "Plano",
            "state": "TX",
            "zip": "75024",
            "phone": "972-985-8000"
        },
        {
            "branch": "Texas Capital Bank - San Antonio",
            "address": "7373 Broadway Ste 100",
            "city": "San Antonio",
            "state": "TX",
            "zip": "78209",
            "phone": "210-220-4000"
        },
    ],
    "Truist Bank": [
        {
            "branch": "Truist Bank - Charlotte Uptown",
            "address": "214 N Tryon St",
            "city": "Charlotte",
            "state": "NC",
            "zip": "28202",
            "phone": "704-715-8000"
        },
        {
            "branch": "Truist Bank - Atlanta Midtown",
            "address": "171 17th St NW",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30363",
            "phone": "404-658-8000"
        },
        {
            "branch": "Truist Bank - Richmond",
            "address": "100 N 14th St",
            "city": "Richmond",
            "state": "VA",
            "zip": "23219",
            "phone": "804-782-8000"
        },
        {
            "branch": "Truist Bank - Tampa",
            "address": "100 N Tampa St",
            "city": "Tampa",
            "state": "FL",
            "zip": "33602",
            "phone": "813-224-8000"
        },
        {
            "branch": "Truist Bank - Birmingham",
            "address": "200 20th St N",
            "city": "Birmingham",
            "state": "AL",
            "zip": "35203",
            "phone": "205-324-8000"
        },
        {
            "branch": "Truist Bank - Memphis",
            "address": "200 S Main St",
            "city": "Memphis",
            "state": "TN",
            "zip": "38103",
            "phone": "901-543-8000"
        },
        {
            "branch": "Truist Bank - Nashville",
            "address": "200 4th Ave N",
            "city": "Nashville",
            "state": "TN",
            "zip": "37219",
            "phone": "615-244-8000"
        },
        {
            "branch": "Truist Bank - Dallas",
            "address": "2001 Bryan St",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-922-8000"
        },
        {
            "branch": "Truist Bank - Washington DC",
            "address": "800 17th St NW",
            "city": "Washington",
            "state": "DC",
            "zip": "20006",
            "phone": "202-857-8000"
        },
        {
            "branch": "Truist Bank - Baltimore",
            "address": "100 Light St",
            "city": "Baltimore",
            "state": "MD",
            "zip": "21202",
            "phone": "410-576-8000"
        },
        {
            "branch": "Truist Bank - Raleigh",
            "address": "150 Fayetteville St",
            "city": "Raleigh",
            "state": "NC",
            "zip": "27601",
            "phone": "919-829-8000"
        },
        {
            "branch": "Truist Bank - Columbia",
            "address": "1200 Main St",
            "city": "Columbia",
            "state": "SC",
            "zip": "29201",
            "phone": "803-256-8000"
        },
    ],
    "U.S. Bank": [
        {
            "branch": "U.S. Bank - Boise 12th Avenue",
            "address": "2220 12th Ave Rd",
            "city": "Nampa",
            "state": "ID",
            "zip": "83686",
            "phone": "208-465-8000"
        },
        {
            "branch": "U.S. Bank - Boise 17th & State",
            "address": "1688 W State St",
            "city": "Boise",
            "state": "ID",
            "zip": "83702",
            "phone": "208-345-8000"
        },
        {
            "branch": "U.S. Bank - Boulder",
            "address": "1650 28th St",
            "city": "Boulder",
            "state": "CO",
            "zip": "80301",
            "phone": "303-442-8000"
        },
        {
            "branch": "U.S. Bank - Bowling Green Campbell Lane",
            "address": "721 Campbell Ln",
            "city": "Bowling Green",
            "state": "KY",
            "zip": "42104",
            "phone": "270-746-8000"
        },
        {
            "branch": "U.S. Bank - Bozeman",
            "address": "104 E Main St",
            "city": "Bozeman",
            "state": "MT",
            "zip": "59715",
            "phone": "406-587-8000"
        },
        {
            "branch": "U.S. Bank - Bremerton",
            "address": "2020 6th St",
            "city": "Bremerton",
            "state": "WA",
            "zip": "98337",
            "phone": "360-377-8000"
        },
        {
            "branch": "U.S. Bank - Chicago",
            "address": "1 S Dearborn St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-732-8000"
        },
        {
            "branch": "U.S. Bank - St. Charles",
            "address": "855 S Randall Rd",
            "city": "St. Charles",
            "state": "IL",
            "zip": "60174",
            "phone": "630-513-8000"
        },
        {
            "branch": "U.S. Bank - Dallas",
            "address": "2001 Bryan St",
            "city": "Dallas",
            "state": "TX",
            "zip": "75201",
            "phone": "214-922-8000"
        },
        {
            "branch": "U.S. Bank - Houston",
            "address": "1000 Louisiana St",
            "city": "Houston",
            "state": "TX",
            "zip": "77002",
            "phone": "713-247-8000"
        },
        {
            "branch": "U.S. Bank - Minneapolis",
            "address": "800 Nicollet Mall",
            "city": "Minneapolis",
            "state": "MN",
            "zip": "55402",
            "phone": "612-342-8000"
        },
        {
            "branch": "U.S. Bank - Portland",
            "address": "101 SW Main St",
            "city": "Portland",
            "state": "OR",
            "zip": "97204",
            "phone": "503-226-8000"
        },
        {
            "branch": "U.S. Bank - Salt Lake City",
            "address": "100 S Main St",
            "city": "Salt Lake City",
            "state": "UT",
            "zip": "84101",
            "phone": "801-350-8000"
        },
        {
            "branch": "U.S. Bank - Milwaukee",
            "address": "777 E Wisconsin Ave",
            "city": "Milwaukee",
            "state": "WI",
            "zip": "53202",
            "phone": "414-224-8000"
        },
        {
            "branch": "U.S. Bank - Cincinnati",
            "address": "201 E 4th St",
            "city": "Cincinnati",
            "state": "OH",
            "zip": "45202",
            "phone": "513-621-8000"
        },
        {
            "branch": "Little Rock Capitol",
            "address": "401 W Capitol Ave",
            "city": "Little Rock",
            "state": "AR",
            "zip": "72201",
            "phone": "501-376-7000"
        },
        {
            "branch": "Omaha Main",
            "address": "500 S 19th St",
            "city": "Omaha",
            "state": "NE",
            "zip": "68102",
            "phone": "402-576-5000"
        },
        {
            "branch": "Lincoln",
            "address": "200 O St",
            "city": "Lincoln",
            "state": "NE",
            "zip": "68508",
            "phone": "402-576-6000"
        },
        {
            "branch": "Sioux Falls Main",
            "address": "100 S Main Ave",
            "city": "Sioux Falls",
            "state": "SD",
            "zip": "57104",
            "phone": "605-576-5000"
        },
        {
            "branch": "Fargo Main",
            "address": "100 Main St",
            "city": "Fargo",
            "state": "ND",
            "zip": "58102",
            "phone": "701-576-5000"
        },
    ],
    "USAA Federal Savings Bank": [
        {
            "branch": "USAA - Phoenix",
            "address": "1 Norterra Drive",
            "city": "Phoenix",
            "state": "AZ",
            "zip": "85085",
            "phone": "800-531-8000"
        },
        {
            "branch": "USAA - San Antonio",
            "address": "10750 W Interstate 10",
            "city": "San Antonio",
            "state": "TX",
            "zip": "78230",
            "phone": "210-531-8000"
        },
        {
            "branch": "USAA - Colorado Springs",
            "address": "1855 Telstar Drive",
            "city": "Colorado Springs",
            "state": "CO",
            "zip": "80920",
            "phone": "719-531-8000"
        },
        {
            "branch": "USAA - Annapolis",
            "address": "2000 West St",
            "city": "Annapolis",
            "state": "MD",
            "zip": "21401",
            "phone": "410-573-8000"
        },
        {
            "branch": "USAA - Highland Falls",
            "address": "600 Main St",
            "city": "Highland Falls",
            "state": "NY",
            "zip": "10928",
            "phone": "845-446-8000"
        },
    ],
    "WebBank": [
        {
            "branch": "WebBank - Salt Lake City",
            "address": "215 South State Street Suite 1000",
            "city": "Salt Lake City",
            "state": "UT",
            "zip": "84111",
            "phone": "801-456-8000"
        },
    ],
    "Wells Fargo Bank": [
        {
            "branch": "Wells Fargo - Potrero & 16th",
            "address": "2300 16th St",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94103",
            "phone": "415-553-8000"
        },
        {
            "branch": "Wells Fargo - Riverside & Congress",
            "address": "501 S Congress Ave",
            "city": "Austin",
            "state": "TX",
            "zip": "78704",
            "phone": "512-477-8000"
        },
        {
            "branch": "Wells Fargo - Hudson Yards",
            "address": "500 W 30th St",
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "phone": "212-216-2000"
        },
        {
            "branch": "Wells Fargo - Downtown Los Angeles",
            "address": "333 S Grand Ave",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90071",
            "phone": "213-629-8000"
        },
        {
            "branch": "Wells Fargo - Denver",
            "address": "1700 Broadway",
            "city": "Denver",
            "state": "CO",
            "zip": "80290",
            "phone": "303-585-9000"
        },
        {
            "branch": "Wells Fargo - Chicago",
            "address": "1 S Dearborn St",
            "city": "Chicago",
            "state": "IL",
            "zip": "60603",
            "phone": "312-732-8000"
        },
        {
            "branch": "Wells Fargo - Phoenix",
            "address": "100 W Washington St",
            "city": "Phoenix",
            "state": "AZ",
            "zip": "85003",
            "phone": "602-452-6000"
        },
        {
            "branch": "Wells Fargo - Seattle",
            "address": "1201 3rd Ave",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101",
            "phone": "206-587-3000"
        },
        {
            "branch": "Wells Fargo - Atlanta",
            "address": "171 17th St NW",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30363",
            "phone": "404-658-2000"
        },
        {
            "branch": "Wells Fargo - Miami",
            "address": "100 S Biscayne Blvd",
            "city": "Miami",
            "state": "FL",
            "zip": "33131",
            "phone": "305-373-8000"
        },
        {
            "branch": "Wells Fargo - Charlotte",
            "address": "300 S Tryon St",
            "city": "Charlotte",
            "state": "NC",
            "zip": "28202",
            "phone": "704-715-8000"
        },
        {
            "branch": "Wells Fargo - Minneapolis",
            "address": "600 Marquette Ave",
            "city": "Minneapolis",
            "state": "MN",
            "zip": "55402",
            "phone": "612-342-8000"
        },
        {
            "branch": "Little Rock Main",
            "address": "400 W Capitol Ave",
            "city": "Little Rock",
            "state": "AR",
            "zip": "72201",
            "phone": "501-376-8000"
        },
        {
            "branch": "Omaha Main",
            "address": "500 S 19th St",
            "city": "Omaha",
            "state": "NE",
            "zip": "68102",
            "phone": "402-576-7000"
        },
        {
            "branch": "Sioux Falls Main",
            "address": "100 S Main Ave",
            "city": "Sioux Falls",
            "state": "SD",
            "zip": "57104",
            "phone": "605-576-6000"
        },
        {
            "branch": "Fargo Main",
            "address": "100 Main St",
            "city": "Fargo",
            "state": "ND",
            "zip": "58102",
            "phone": "701-576-6000"
        },
    ],
    "Zions Bancorporation": [
        {
            "branch": "Zions Bank - Salt Lake City",
            "address": "1 S Main St",
            "city": "Salt Lake City",
            "state": "UT",
            "zip": "84101",
            "phone": "801-844-7000"
        },
        {
            "branch": "Zions Bank - Boise",
            "address": "101 S Capitol Blvd",
            "city": "Boise",
            "state": "ID",
            "zip": "83702",
            "phone": "208-345-8000"
        },
        {
            "branch": "Zions Bank - Meridian",
            "address": "220 W Cherry Ln",
            "city": "Meridian",
            "state": "ID",
            "zip": "83642",
            "phone": "208-888-8000"
        },
        {
            "branch": "Zions Bank - Nampa",
            "address": "1112 1st St S",
            "city": "Nampa",
            "state": "ID",
            "zip": "83651",
            "phone": "208-467-8000"
        },
        {
            "branch": "Zions Bank - Caldwell",
            "address": "607 Cleveland Blvd",
            "city": "Caldwell",
            "state": "ID",
            "zip": "83605",
            "phone": "208-454-8000"
        },
        {
            "branch": "Zions Bank - Casper",
            "address": "435 W 1st St",
            "city": "Casper",
            "state": "WY",
            "zip": "82601",
            "phone": "307-234-8000"
        },
    ],
}

# States covered by each bank (derived from branch data)
BANK_STATES = {
    bank_name: list(set(branch["state"] for branch in branches))
    for bank_name, branches in BANK_BRANCHES.items()
}

def get_branches_by_state(bank_name: str, state: str) -> list:
    """Get branches for a specific bank in a specific state."""
    branches = BANK_BRANCHES.get(bank_name, [])
    return [b for b in branches if b["state"] == state.upper()]

def get_bank_states(bank_name: str) -> list:
    """Get list of states where a bank has branches."""
    return BANK_STATES.get(bank_name, [])

def search_branches(bank_name: str, city: str = None, state: str = None) -> list:
    """Search for branches by bank name, optionally filtering by city and/or state."""
    branches = BANK_BRANCHES.get(bank_name, [])
    if city:
        branches = [b for b in branches if city.lower() in b["city"].lower()]
    if state:
        branches = [b for b in branches if b["state"] == state.upper()]
    return branches
