# Tasks
- only use data upto June, 2024 for head to head calculation, else disqualification!
    - this implies recalculation of some datasets
- model banao fatafat
- UI-api connect karo
- add SHAP explainability to recommended team!
- mohammad nawaz and mohammad nawaz (3) are the same person!
    - [line: 58](./CSVs/Designation.csv) 3086f7a4,Mohammad Nawaz (3),Bowler
    - [line: 4034](./CSVs/Designation.csv) 3086f7a4,Mohammad Nawaz,Bowler

- Hall of shame:
    - Sohit -> HeadToHead dataset not given even after one week passed!
    - Chaitanya -> Passed correlated features into model, realised it but still didn't fix till the last day
    - Harsh -> Data inconsistencies! (Venues)
    - Harsh -> Error while loading model because of wrong order of columns in career, recent_form and venue CSVs
    - Meet -> committed 18000 json files (1st commit) for no reason
    - Shubham -> Rohit Sharma is in great form against India
    - Vraj -> passing extra parameters for calculating dream team in  calculating_dream_team()
    - Chaitanya -> generate_recommended_team changed (over representation or some shit)
