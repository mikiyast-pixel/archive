The Archive

Pair: Mikiyas Tesfay & Ally
Repository: https://github.com/mikiyast-pixel/archive

--------------------------------------------------

1. The record

id | String | Example: MS001 | If unknown: Reject the record during validation (cannot index without a valid primary key).
title | String | Example: Tarikh al-Sudan | If unknown: Reject the record during validation (unidentifiable manuscript).
city | String | Example: Timbuktu | If unknown: Reject the record during validation (outside catalogued geographic origin scope).
year | String (Integer) | Example: 1655 | If unknown: Reject the record during validation (cannot place manuscript in chronological order).
condition | String | Example: fragile | If unknown: Reject the record during validation (preservation status is mandatory for archiving).

--------------------------------------------------

2. Our validation rules

id: Must start with uppercase 'MS' followed by exactly 3 digits (total 5 characters). Rejects: ms001, MS1, XX001
title: Must be present and at least 3 characters long once whitespace is stripped. Rejects: "", "   ", "Ab"
city: Must be present and match one of KNOWN_CITIES (Timbuktu, Djenne, Gao, Walata, Chinguetti), case-insensitively. Rejects: "Kano", "", "Cairo"
year: Must be present, strictly numeric, and fall between 1100 and 1900 inclusive. Rejects: "1099", "1901", "c.1590"
condition: Must be present and match one of VALID_CONDITIONS (fragile, fair, good), case-insensitively. Rejects: "excellent", "broken", ""

Who decided the year range?

We decided to go with the 1100-1900 bounds for this system because they fit real well with the main historical period of manuscript production across Sahelian hubs like Timbuktu and Djenne. That said, setting hard cutoffs definitely comes with a trade-off: it ends up throwing out late 19th/20th-century copies, modern restoration records, and pre-1100 early Islamic codices. If we expand this system down the road, we should probably broaden the lower bound to cover older West African trade route documents too.

--------------------------------------------------

3. The c.1590 decision

Our choice: (a) Reject it. Only exact years enter the catalogue.

Why: Keeping things strictly to integer years keeps query functions like count_before() and oldest() clean and reliable, without us needing to build messy string-parsing logic or overhaul our schema for a basic 5-field CSV file.

What it costs us: The downside is that we have to drop valid historical documents (like entry MS009 in messy.csv) where scholars only have approximate decade estimates, trading off a bit of archive completeness for technical simplicity.

--------------------------------------------------

4. Our test table

validate_year
Normal | Value: 1655 | Expected: valid | Actual: valid | Pass? Yes
Abnormal | Value: c.1590 | Expected: invalid | Actual: invalid | Pass? Yes
Extreme (low) | Value: 1100 | Expected: valid | Actual: valid | Pass? Yes
Extreme (high) | Value: 1900 | Expected: valid | Actual: valid | Pass? Yes
Boundary (below) | Value: 1099 | Expected: invalid | Actual: invalid | Pass? Yes
Boundary (above) | Value: 1901 | Expected: invalid | Actual: invalid | Pass? Yes

validate_condition
Normal | Value: fragile | Expected: valid | Actual: valid | Pass? Yes
Abnormal | Value: excellent | Expected: invalid | Actual: invalid | Pass? Yes
Extreme (case) | Value: GOOD | Expected: valid | Actual: valid | Pass? Yes
Boundary (empty) | Value: "" | Expected: invalid | Actual: invalid | Pass? Yes

--------------------------------------------------

5. Collaboration reflection

Mikiyas Tesfay: Something Ally did that im definitely stealing for future projects is making super short-lived feature branches for quick bug fixes. One thing I'd change next time though is setting up clear branch naming rules early on so we dont get confused with remote branches syncing up weirdly.

Ally: One neat thing Mikiyas did that I want to adopt is breaking down validation rules into small, re-usable helper predicates (like is_null and is_int). Looking back, I should've done code reviews directly on pull request diffs as we went along, rather than trying to review huge batches of commits right at the end.

--------------------------------------------------

6. Declaration

[x] Both of us can explain every line in this repository.
[x] AI assistants used for explanation only, not to generate our implementation or our tests.

If you used an AI assistant, say what you asked and what you did with the answer:
We asked an AI assistant to clarify some confusion in our Git terminal output regarding detached HEAD states and tracking remote branches, as well as the practical difference between .strip() and .rstrip("\r\n") when stripping line endings from CSV files in Python. We used those explanations to fix our local git setup and tweak our line parsing logic.

--------------------------------------------------

Running this project

pytest -v                               # all tests
pytest tests/test_provided.py -v       # the given suite
pytest tests/test_yours.py -v          # your suite
python tools/check_collaboration.py    # your Part C report
