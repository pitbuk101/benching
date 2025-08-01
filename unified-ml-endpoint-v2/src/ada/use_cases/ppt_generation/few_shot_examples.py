"""PPT generation use case, examples of few shot tasks."""

# flake8: noqa: E501

few_shot_examples = {
    "cleaning_title_insights": [
        {
            "user_question": "What is spend by regions?",
            "summarized_output": """
The spend by region for the category Bearings for the current year is as follows:

1. European Union: €1,811,187,874.41
2. Northern America: €99,457,845.25
3. Eastern Asia: €150,251,541.35
4. Southern Asia: €37,743,720.00
5. South America: €33,574,015.48
6. Western Asia: €22,646,696.27
7. South-Eastern Asia: €11,213,688.09
8. Southern Africa: €15,566,341.75
9. Western Europe: €8,464,482.15
10. Eastern Europe: €1,613,351.36
11. Australia and New Zealand: €646,484.31
12. Eastern Africa: €243,778.35
13. Central America: €111,357.61
14. Northern Africa: €46,438.00

Please note that these figures are in descending order of spend.""",
            "currency": "EUR",
            "chart_type": "bar",
            "input_data": """[
{"Supplier country[txt_region]":"#","[TotalSpend]":1958040.9993001595},
{"Supplier country[txt_region]":"Western Asia","[TotalSpend]":22646696.266329445},
{"Supplier country[txt_region]":"Southern Asia","[TotalSpend]":37743720.002317384},
{"Supplier country[txt_region]":"South America","[TotalSpend]":33574015.4780478},
{"Supplier country[txt_region]":"European Union","[TotalSpend]":1811181874.4092522},
{"Supplier country[txt_region]":"Australia and New Zealand","[TotalSpend]":646484.3096904571},
{"Supplier country[txt_region]":"Eastern Africa","[TotalSpend]":243778.34610000002},
{"Supplier country[txt_region]":"Northern America","[TotalSpend]":99457845.24878387},
{"Supplier country[txt_region]":"South-Eastern Asia","[TotalSpend]":11213688.09493465},
{"Supplier country[txt_region]":"Southern Africa","[TotalSpend]":15566341.750055911},
{"Supplier country[txt_region]":"Eastern Europe","[TotalSpend]":1613351.3607},
{"Supplier country[txt_region]":"Central America","[TotalSpend]":111357.60893654801},
{"Supplier country[txt_region]":"Western Europe","[TotalSpend]":8464482.146351997},
{"Supplier country[txt_region]":"Eastern Asia","[TotalSpend]":150251541.3547108},
{"Supplier country[txt_region]":"Northern Africa","[TotalSpend]":46438}]""",
            "output": '''{
"cleaned_data": """
{
"categories": ["#","Western Asia","Southern Asia","South America","European Union","Australia and New Zealand","Eastern Africa","Northern America","South-Eastern Asia","Southern Africa","Eastern Europe","Central America","Western Europe","Eastern Asia","Northern Africa"],
"series": [
    ('TotalSpend', (1958040.99930015, 22646696.2663294, 37743720.0023173, 33574015.4780478, 1811181874.40925, 646484.309690457, 243778.3461, 99457845.2487838, 11213688.0949346, 15566341.7500559, 1613351.3607, 111357.608936548, 8464482.14635199, 150251541.35471, 46438)),
]
}
""",
"title": "European Union dominates spend with EUR 1.81 Bn",
"insights": """["European Union captures 83% of the total spend.",
"Top 3 regions account for 94% of the total spend, indicating a high concentration of spend.",
"Negligible spend in Central America and Northern Africa highlights a minimal supplier base.",
"High regional concentration signals a potential for greater supplier diversification."]""",
"chart_title": "Spend distribution by region for the current year, EUR Mn",
"rounding": "Mn",
}''',
        },
        {
            "user_question": "what are my top 5 suppliers?",
            "summarized_output": """The top 5 suppliers for the current year are:

1. SKF FRANCE with a total spend of EUR 14,212,045.61
2. Heinrich Jungeblodt GmbH & Co.KG special screws with a total spend of EUR 3,307,463.66
3. GBM SARL with a total spend of EUR 8,541,042.01
4. CNC manufacturing technology Friedemann with a total spend of EUR 7,472,284.22
5. PTP INDUSTRY SAS with a total spend of EUR 2,822,224.14

Please note that these figures are calculated based on the data available for the current year.""",
            "currency": "EUR",
            "chart_type": "bar",
            "input_data": """
            [{"Supplier[TXT_SUPPLIER]":"PTP INDUSTRY SAS","[TotalSpend]":2822224.135500001},
{"Supplier[TXT_SUPPLIER]":"Heinrich Jungeblodt GmbH & Co.KG special screws","[TotalSpend]":3307463.657099996},
{"Supplier[TXT_SUPPLIER]":"SKF FRANCE","[TotalSpend]":14212045.613400001},
{"Supplier[TXT_SUPPLIER]":"CNC manufacturing technology Friedemann","[TotalSpend]":7472284.223999999},
{"Supplier[TXT_SUPPLIER]":"GBM SARL","[TotalSpend]":8541042.0075}]""",
            "output": '''{
"cleaned_data": """
{
"categories": ["PTP INDUSTRY SAS", "Heinrich Jungeblodt GmbH & Co.KG special screws", "SKF FRANCE", "CNC manufacturing technology Friedemann", "GBM SARL"],
"series": [
    ('TotalSpend', (2822224.1355, 3307463.65709999, 14212045.6134, 7472284.22399999, 8541042.0075)),
]
}

""",
"title": "SKF FRANCE is the top supplier with a total spend of EUR 14.21 Mn",
"insights": """["SKF FRANCE leads the supplier list with 39% of top 5 suppliers spend.",
"GBM SARL and CNC manufacturing technology Friedemann follow closely with spends of 23% and 21% respectively.",
"PTP INDUSTRY SAS has the least spend among the top 5 suppliers with 8% of the spend."]""",
"chart_title": "Top 5 suppliers by total spend for the current year, EUR Mn",
"rounding": "Mn",
}''',
        },
        {
            "user_question": "What is my cost distribution across this category",
            "summarized_output": """The cost distribution is as follows:
- Carbon Steel: 30.74% of total cost
- Labor: 28% of total cost
- Stainless Steel: 14.31% of total cost
- Copper and Copper Semis: 4.77% of total cost
- R&D: 9% of total cost
- Overheads: 7% of total cost
- Aluminum: 2.12% of total cost
- Utilities: 3% of total cost
- Tin: 1.06% of total cost

Please note that these calculations are for the current year and are in EUR.""",
            "currency": "EUR",
            "chart_type": "pie",
            "input_data": """
[{"Fact market cost structure new[TXT_COMPONENT_NAME]":"R&D","[Share]":0.09},
{"Fact market cost structure new[TXT_COMPONENT_NAME]":"Labor","[Share]":0.28},
{"Fact market cost structure new[TXT_COMPONENT_NAME]":"Utilities","[Share]":0.03},
{"Fact market cost structure new[TXT_COMPONENT_NAME]":"Overheads","[Share]":0.07},
{"Fact market cost structure new[TXT_COMPONENT_NAME]":"Tin","[Share]":0.0106},
{"Fact market cost structure new[TXT_COMPONENT_NAME]":"Stainless Steel","[Share]":0.1431},
{"Fact market cost structure new[TXT_COMPONENT_NAME]":"Aluminum","[Share]":0.0212},
{"Fact market cost structure new[TXT_COMPONENT_NAME]":"Copper and Copper Semis","[Share]":0.0477},
{"Fact market cost structure new[TXT_COMPONENT_NAME]":"Carbon Steel","[Share]":0.3074}]""",
            "output": '''
            {
"cleaned_data": """
{
"categories": ["R&D", "Labor", "Utilities", "Overheads", "Tin", "Stainless Steel", "Aluminum", "Copper and Copper Semis", "Carbon Steel"],
"series": [
    ("Share", (0.09, 0.28, 0.03, 0.07, 0.0106, 0.1431, 0.0212, 0.0477, 0.3074))
]
}
""",
"title": "Carbon Steel constitutes the largest share in cost structure with 30% of total cost",
"insights": """["Top 3 components contribute 72% of the total cost, indicating a concentrated cost structure.",
"Carbon Steel dominates the cost structure, followed by Labor and Stainless Steel."]""",
"chart_title": "Cost distribution in % share for the current year",
"rounding": "None"
}''',
        },
        {
            "user_question": "What is global revenue breakup by product type for the"
            " quarter 2022 Q4?",
            "summarized_output": """The global revenue breakup by product type for
             the quarter 2022 Q4 is as follows:

- Globe: 22%
- Ball: 21%
- Gate: 20%
- Butterfly: 15%
- Plug: 10%
- Safety Relief: 5%
- Check: 4%
- Others: 3%

Please note that these percentages represent the
 proportion of total global revenue generated by each product type.""",
            "currency": "EUR",
            "chart_type": "pie",
            "input_data": """
[{"Market segmentation[TXT_SEGMENTATION]":"Globe","Fact market demand supply segmentation[DIM_UOM]":"Percent","[value]":22},
{"Market segmentation[TXT_SEGMENTATION]":"Ball","Fact market demand supply segmentation[DIM_UOM]":"Percent","[value]":21},
{"Market segmentation[TXT_SEGMENTATION]":"Gate","Fact market demand supply segmentation[DIM_UOM]":"Percent","[value]":20},
{"Market segmentation[TXT_SEGMENTATION]":"Butterfly","Fact market demand supply segmentation[DIM_UOM]":"Percent","[value]":15},
{"Market segmentation[TXT_SEGMENTATION]":"Plug","Fact market demand supply segmentation[DIM_UOM]":"Percent","[value]":10},
{"Market segmentation[TXT_SEGMENTATION]":"Safety Relief","Fact market demand supply segmentation[DIM_UOM]":"Percent","[value]":5},
{"Market segmentation[TXT_SEGMENTATION]":"Check","Fact market demand supply segmentation[DIM_UOM]":"Percent","[value]":4},
{"Market segmentation[TXT_SEGMENTATION]":
"Others","Fact market demand supply segmentation[DIM_UOM]":"Percent","[value]":3}]""",
            "output": '''
     {
         "cleaned_data": """
{
"categories": ["Globe", "Ball", "Gate", "Butterfly", "Plug", "Safety Relief", "Check", "Others"],
"series": [('Percent', (22, 21, 20, 15, 10, 5, 4, 3))]
}""",
"title": "Globe leads global revenue by product type with 22% in 2022 Q4",
"insights": """["Globe, Ball, and Gate products account for 63% of total revenue, indicating a strong market presence.",
"Butterfly and Plug products contribute 25% of the total revenue, reflecting a balanced product mix."]""",
"chart_title": "Global revenue breakup by product type for 2022 Q4, %",

"rounding": "None"
     }''',
        },
        {
            "user_question": "what is my spend by region and quarter for 2023",
            "summarized_output": """The spend by region and quarter for the year 2023 is as follows:

In the European Union, the spend was as follows:
- In Q4, the spend was €29,704,819.32
- In Q2, the spend was €28,739,637.53
- In Q3, the spend was €28,221,565.16
- In Q1, the spend was €26,914,119.56

In Northern America, the spend in Q2 was €2,919,654.70.

In South America, the spend was as follows:
- In Q1, the spend was €2,747,826.69
- In Q4, the spend was €2,461,237.08

In Eastern Asia, the spend was as follows:
- In Q2, the spend was €2,624,791.31
- In Q3, the spend was €2,447,874.65
- In Q1, the spend was €2,232,785.32

Please note that these calculations are done for the category Bearings.""",
            "currency": "EUR",
            "chart_type": "stacked",
            "input_data": """
[{"Supplier country[txt_region]":"#","Period[TXT_QUARTER]":"2023 Q2","[TotalSpend]":5576.436012751036},
{"Supplier country[txt_region]":"#","Period[TXT_QUARTER]":"2023 Q4","[TotalSpend]":2540.9786569438397},
{"Supplier country[txt_region]":"Western Asia","Period[TXT_QUARTER]":"2023 Q1","[TotalSpend]":575104.7547845328},
{"Supplier country[txt_region]":"Western Asia","Period[TXT_QUARTER]":"2023 Q2","[TotalSpend]":954708.1770735132},
{"Supplier country[txt_region]":"Western Asia","Period[TXT_QUARTER]":"2023 Q3","[TotalSpend]":1916390.9033951221},
{"Supplier country[txt_region]":"Western Asia","Period[TXT_QUARTER]":"2023 Q4","[TotalSpend]":923452.0805157654},
{"Supplier country[txt_region]":"Southern Asia","Period[TXT_QUARTER]":"2023 Q1","[TotalSpend]":1480945.9565491467},
{"Supplier country[txt_region]":"Southern Asia","Period[TXT_QUARTER]":"2023 Q2","[TotalSpend]":904514.6583511115},
{"Supplier country[txt_region]":"Southern Asia","Period[TXT_QUARTER]":"2023 Q3","[TotalSpend]":730682.9872341823},
{"Supplier country[txt_region]":"Southern Asia","Period[TXT_QUARTER]":"2023 Q4","[TotalSpend]":598073.3857154247},
{"Supplier country[txt_region]":"Latin America and the Caribbean","Period[TXT_QUARTER]":"2023 Q4","[TotalSpend]":7213.512000000001},
{"Supplier country[txt_region]":"South America","Period[TXT_QUARTER]":"2023 Q1","[TotalSpend]":2747826.687897014},
{"Supplier country[txt_region]":"South America","Period[TXT_QUARTER]":"2023 Q2","[TotalSpend]":2158060.7992984536},
{"Supplier country[txt_region]":"South America","Period[TXT_QUARTER]":"2023 Q3","[TotalSpend]":1282618.3503535714},
{"Supplier country[txt_region]":"South America","Period[TXT_QUARTER]":"2023 Q4","[TotalSpend]":2461237.082829024},
{"Supplier country[txt_region]":"European Union","Period[TXT_QUARTER]":"2023 Q1","[TotalSpend]":26914119.558388427},
{"Supplier country[txt_region]":"European Union","Period[TXT_QUARTER]":"2023 Q2","[TotalSpend]":28739637.53166531},
{"Supplier country[txt_region]":"European Union","Period[TXT_QUARTER]":"2023 Q3","[TotalSpend]":28221565.157016147},
{"Supplier country[txt_region]":"European Union","Period[TXT_QUARTER]":"2023 Q4","[TotalSpend]":29704819.315418404},
{"Supplier country[txt_region]":"Northern America","Period[TXT_QUARTER]":"2023 Q1","[TotalSpend]":1103235.3077110678},
{"Supplier country[txt_region]":"Northern America","Period[TXT_QUARTER]":"2023 Q2","[TotalSpend]":2919654.6957754144},
{"Supplier country[txt_region]":"Northern America","Period[TXT_QUARTER]":"2023 Q3","[TotalSpend]":939111.7333604506},
{"Supplier country[txt_region]":"Northern America","Period[TXT_QUARTER]":"2023 Q4","[TotalSpend]":2008333.7674116478},
{"Supplier country[txt_region]":"Southern Africa","Period[TXT_QUARTER]":"2023 Q1","[TotalSpend]":82428.21876890346},
{"Supplier country[txt_region]":"Southern Africa","Period[TXT_QUARTER]":"2023 Q2","[TotalSpend]":52651.00381153121},
{"Supplier country[txt_region]":"Southern Africa","Period[TXT_QUARTER]":"2023 Q3","[TotalSpend]":378877.69295273704},
{"Supplier country[txt_region]":"Southern Africa","Period[TXT_QUARTER]":"2023 Q4","[TotalSpend]":283871.10050665634},
{"Supplier country[txt_region]":"Western Europe","Period[TXT_QUARTER]":"2023 Q1","[TotalSpend]":55290.375},
{"Supplier country[txt_region]":"Western Europe","Period[TXT_QUARTER]":"2023 Q2","[TotalSpend]":114040.875},
{"Supplier country[txt_region]":"Western Europe","Period[TXT_QUARTER]":"2023 Q3","[TotalSpend]":69616.6345},
{"Supplier country[txt_region]":"Western Europe","Period[TXT_QUARTER]":"2023 Q4","[TotalSpend]":43569.375},
{"Supplier country[txt_region]":"Eastern Asia","Period[TXT_QUARTER]":"2023 Q1","[TotalSpend]":2232785.315725121},
{"Supplier country[txt_region]":"Eastern Asia","Period[TXT_QUARTER]":"2023 Q2","[TotalSpend]":2624791.3109743986},
{"Supplier country[txt_region]":
"Eastern Asia","Period[TXT_QUARTER]":"2023 Q3","[TotalSpend]":2447874.645462765},
{"Supplier country[txt_region]":"Eastern Asia","Period[TXT_QUARTER]":"2023 Q4",
"[TotalSpend]":1867793.4219669134}]""",
            "output": '''
     {
         "cleaned_data": """
{
"categories": ["2023 Q1", "2023 Q2", "2023 Q3", "2023 Q4"],
"series": [('Western Asia', (575104.7547845328, 954708.1770735132, 1916390.9033951221, 923452.0805157654)),
('Southern Asia', (1480945.9565491467, 904514.6583511115, 730682.9872341823, 598073.3857154247)),
('Latin America and the Caribbean', (0, 0, 0, 7213.512000000001)),
('South America', (2747826.687897014, 2158060.7992984536, 1282618.3503535714, 2461237.082829024)),
('European Union', (26914119.558388427, 28739637.53166531, 28221565.157016147, 29704819.315418404)),
('Northern America', (1103235.3077110678, 2919654.6957754144, 939111.7333604506, 2008333.7674116478)),
('Southern Africa', (82428.21876890346, 52651.00381153121, 378877.69295273704, 283871.10050665634)),
('Western Europe', (55290.375, 114040.875, 69616.6345, 43569.375)),
('Eastern Asia', (2232785.315725121, 2624791.3109743986, 2447874.645462765, 1867793.4219669134))
]
}""",
         "title": "European Union leads in spend across all quarters in 2023",
         "insights": """["European Union consistently leads in spend across all quarters with a total spend of EUR 113 Mn in 2023.",
         "Overall global spend does not show much variation across quarters, indicating stable spending patterns.",
         "There was a sudden dip in spend for South America in Q3, which recovered in Q4.",
         "Northern America saw a significant increase in spend in Q2, followed by a slight decrease in Q3 and Q4."]""",
         ",
         "chart_title": "Quarterly spend by region for 2023, EUR Mn",
         "rounding": "Mn"
     }''',
        },
        {
            "user_question": "What is spend in last 10 months",
            "summarized_output": """The total spend for the category Bearings in
             the last 10 months is as follows:

- December 2023: EUR 15,494,026.12
- November 2023: EUR 10,979,600.02
- October 2023: EUR 11,427,277.88
- September 2023: EUR 11,193,844.53
- August 2023: EUR 11,832,230.42
- July 2023: EUR 12,960,663.16
- June 2023: EUR 12,847,144.18
- May 2023: EUR 11,489,491.60
- April 2023: EUR 14,136,999.71
- March 2023: EUR 12,166,543.34

Please note that these calculations are done for the category Bearings.""",
            "currency": "EUR",
            "chart_type": "line",
            "input_data": """
[{"Period[Month Name]":"March","Period[TXT_YEAR]":2023,"[TotalSpend]":12166543.339019084},
{"Period[Month Name]":"April","Period[TXT_YEAR]":2023,"[TotalSpend]":14136999.708822364},
{"Period[Month Name]":"May","Period[TXT_YEAR]":2023,"[TotalSpend]":11489491.596448926},
{"Period[Month Name]":"June","Period[TXT_YEAR]":2023,"[TotalSpend]":12847144.182691341},
{"Period[Month Name]":"July","Period[TXT_YEAR]":2023,"[TotalSpend]":12960663.156388886},
{"Period[Month Name]":"August","Period[TXT_YEAR]":2023,"[TotalSpend]":11832230.416873697},
{"Period[Month Name]":"September","Period[TXT_YEAR]":2023,"[TotalSpend]":11193844.531012453},
{"Period[Month Name]":"October","Period[TXT_YEAR]":2023,"[TotalSpend]":11427277.881594557},
{"Period[Month Name]":"November","Period[TXT_YEAR]":2023,"[TotalSpend]":10979600.020290831},
{"Period[Month Name]":"December","Period[TXT_YEAR]":2023,"[TotalSpend]":15494026.1181355}]
""",
            "output": '''
     {
         "cleaned_data": """
{
"categories": ["March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
"series": [('TotalSpend', (12166543.339019084, 14136999.708822364, 11489491.596448926, 12847144.182691341, 12960663.156388886, 11832230.416873697, 11193844.531012453, 11427277.881594557, 10979600.020290831, 15494026.1181355))]
}""",
         "title": "Spend has increased by 27% over the past 10 months",
         "insights": """["Spending was highest in Dec at 15.49 Mn, increasing 41% from Nov, potentially indicating need for further investigation.",
"Overall trend across 10 months that mostly its been roughly stable with anomalies in April and December."]""",
"chart_title": "Monthly Total Spend in 2023, EUR Mn",
         "rounding": "Mn"
     }''',
        },
        {
            "user_question": "what is the spend and quantity quarter wise for last 3 years?",
            "summarized_output": """The spend and quantity for Bearings category quarter wise
            for the last 3 years are as follows:

For 2023 Q4, the total spend was €537,498,289.86 and the total quantity was 266,288,964.90.
For 2023 Q3, the total spend was €542,149,337.33 and the total quantity was 294,175,987.51.
For 2023 Q2, the total spend was €556,421,262.11 and the total quantity was 274,705,617.22.
For 2023 Q1, the total spend was €558,650,766.09 and the total quantity was 332,762,362.32.
For 2022 Q4, the total spend was €1,447,933,613.28 and the total quantity was 232,607,025.61.
For 2022 Q3, the total spend was €573,604,689.90 and the total quantity was 340,367,814.95.
For 2022 Q2, the total spend was €718,462,951.97 and the total quantity was 248,638,208.41.
For 2022 Q1, the total spend was €1,024,875,754.85 and the total quantity was 244,682,207.57.
For 2021 Q4, the total spend was €812,660,156.15 and the total quantity was 321,401,716.67.
For 2021 Q3, the total spend was €540,331,019.05 and the total quantity was 486,131,838.61.""",
            "currency": "EUR",
            "chart_type": "line",
            "input_data": """
[{"Period[TXT_QUARTER]":"2021 Q3","[TotalSpend]":540331019.0488598,"[TotalQuantity]":486131838.6120001},
{"Period[TXT_QUARTER]":"2021 Q4","[TotalSpend]":812660156.1489689,"[TotalQuantity]":321401716.6710001},
{"Period[TXT_QUARTER]":"2022 Q1","[TotalSpend]":1024875754.8525864,"[TotalQuantity]":244682207.56899995},
{"Period[TXT_QUARTER]":"2022 Q2","[TotalSpend]":718462951.9682131,"[TotalQuantity]":248638208.4060001},
{"Period[TXT_QUARTER]":"2022 Q3","[TotalSpend]":573604689.8958136,"[TotalQuantity]":340367814.95300037},
{"Period[TXT_QUARTER]":"2022 Q4","[TotalSpend]":1447933613.2788079,"[TotalQuantity]":232607025.6060002},
{"Period[TXT_QUARTER]":"2023 Q1","[TotalSpend]":558650766.0851351,"[TotalQuantity]":332762362.3240008},
{"Period[TXT_QUARTER]":"2023 Q2","[TotalSpend]":556421262.1066477,"[TotalQuantity]":274705617.21800053},
{"Period[TXT_QUARTER]":"2023 Q3","[TotalSpend]":542149337.3254492,"[TotalQuantity]":294175987.50600076},
{"Period[TXT_QUARTER]":"2023 Q4","[TotalSpend]":537498289.8582733,"[TotalQuantity]":266288964.9009999}]
""",
            "output": '''
     {
         "cleaned_data": """
{
"categories": ["2021 Q3","2021 Q4", "2022 Q1", "2022 Q2", "2022 Q3", "2022 Q4", "2023 Q1", "2023 Q2", "2023 Q3", "2023 Q4"],
"series": [('TotalSpend',(540331019.0488598, 812660156.1489689, 1024875754.8525864, 718462951.9682131, 573604689.8958136, 1447933613.2788079, 558650766.0851351, 556421262.1066477, 542149337.3254492, 537498289.8582733)),
('TotalQuantity',(486131838.6120001, 321401716.6710001, 244682207.56899995, 248638208.4060001, 340367814.95300037, 232607025.6060002, 332762362.3240008, 274705617.21800053, 294175987.50600076, 266288964.9009999))]
}""",
         "title": "Spend and quantity show fluctuations across quarters for the last 3 years",
         "insights": """["Spend showed two spikes in 2022 Q1 and 2022 Q4.",
"Total spend peaked in 2022 Q4 with 154% increase from the previous quarter.",
"Inverse correlation between spend and quantity indicate need of further investigation.",
"Quantity across quarter show declining trend."]""",
         "chart_title": "Quarterly Spend and Quantity for the Last 3 Years, EUR Mn",
         "rounding": "Mn"
     }''',
        },
        {
            "user_question": "What is my spend with my top company changed across "
            "the last 10 months",
            "summarized_output": """The top company you have spent with over the last 10 months is
Industrial Processing GmbH. The total spend with this company this year is €314,311,051.18.
This is a decrease compared to the same period last year, when the total spend was €332,110,962.28.
Therefore, the change in spend this year compared to last year is a decrease of €17,799,911.10.
Please note that these calculations are done for the category Bearings.""",
            "currency": "EUR",
            "chart_type": "line",
            "input_data": """
[['[{"[Top company name]":"Industrial Processing GmbH","[Top company spend this year]":314311051.1750001,"[Top company spend last year]":332110962.27500004,"[Change in spend this year compared to last year]":-17799911.099999964}]']]
""",
            "output": '''
     {
         "cleaned_data": """
{
"categories": ["Last Year","This Year", ],
"series": [('Industrial Processing GmbH', (332110962.27500004,314311051.1750001))]
"title": "Spend with top company, Industrial Processing GmbH, decreased by EUR 17.8Mn in the last 10 months",
"insights": """["Spend with Industrial Processing GmbH decreased by 5.36% compared to the previous year.",
"Total spend this year is €314.3Mn, while it was €332.1Mn last year."]""",
"chart_title": "Change in Spend with Industrial Processing GmbH, EUR Mn",
"rounding": "Mn"
}''',
        },
    ],
}
