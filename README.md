# The Archive

**Pair:** Mikiyas Tesfay & Ally  
**Repository:** https://github.com/mikiyast-pixel/archive

---

## 1. The record

| Field | Type | Example | If it is unknown, we… |
| --- | --- | --- | --- |
| id | String | `MS001` | Reject the record during validation (cannot index without a valid primary key). |
| title | String | `Tarikh al-Sudan` | Reject the record during validation (unidentifiable manuscript). |
| city | String | `Timbuktu` | Reject the record during validation (outside catalogued geographic origin scope). |
| year | String (Integer) | `1655` | Reject the record during validation (cannot place manuscript in chronological order). |
| condition | String | `fragile` | Reject the record during validation (preservation status is mandatory for archiving). |

---

## 2. Our validation rules

| Field | Rule(s) | Rejects (example) |
| --- | --- | --- |
| id | Must start with uppercase 'MS' followed by exactly 3 digits (total 5 characters). | `ms001`, `MS1`, `XX001` |
| title | Must be present and at least 3 characters long once leading/trailing whitespace is stripped. | `""`, `"   "`, `"Ab"` |
| city | Must be present and match one of `KNOWN_CITIES` (`Timbuktu`, `Djenne`, `Gao`, `Walata`, `Chinguetti`), case-insensitively. | `"Kano"`, `""`, `"Cairo"` |
| year | Must be present, strictly numeric, and fall between `1100` and `1900` inclusive. | `"1099"`, `"1901"`, `"c.1590"` |
| condition | Must be present and match one of `VALID_CONDITIONS` (`fragile`, `fair`, `good`), case-insensitively. | `"excellent"`, `"broken"`, `""` |

### Who decided the year range?

We accept the `1100–1900` bounds for this specific system because they align with the historical golden age of manuscript production across Sahelian centers like Timbuktu and Djenné. However, this boundary carries a clear cataloguing cost: it throws away late 19th/20th-century copies, modern restorations, and pre-1100 early Islamic codices or epigraphy. If expanding the system in the future, we would widen the lower bound to accommodate earlier West African trade route documents.

---

## 3. The `c.1590` decision

**Our choice:** **(a)** Reject it. Only exact years enter the catalogue.

**Why:** Maintaining integer-strict years preserves reliability across query functions like `count_before()` and `oldest()` without introducing complex string-parsing or schema migrations into a flat 5-field CSV file.

**What it costs us:** It forces the exclusion of valid historical artifacts (like record `MS009` in `messy.csv`) where scholars only possess approximate decade estimates, reducing overall archive completeness in exchange for technical simplicity.

---

## 4. Our test table

### `validate_year`

| Test data | Value | Expected | Actual | Pass? |
| --- | --- | --- | --- | --- |
| Normal | 1655 | valid | valid | Yes |
| Abnormal | c.1590 | invalid | invalid | Yes |
| Extreme (low) | 1100 | valid | valid | Yes |
| Extreme (high) | 1900 | valid | valid | Yes |
| Boundary (below) | 1099 | invalid | invalid | Yes |
| Boundary (above) | 1901 | invalid | invalid | Yes |

### `validate_condition`

| Test data | Value | Expected | Actual | Pass? |
| --- | --- | --- | --- | --- |
| Normal | fragile | valid | valid | Yes |
| Abnormal | excellent | invalid | invalid | Yes |
| Extreme (case) | GOOD | valid | valid | Yes |
| Boundary (empty) | "" | invalid | invalid | Yes |

---

## 5. Collaboration reflection

**Mikiyas Tesfay:** One thing my partner did that I will steal is her habit of creating dedicated, short-lived feature branches for isolated bug fixes. One thing I would do differently next time is establish clear branch naming conventions early on to avoid remote branch mismatch issues.

**Ally:** One thing my partner did that I will steal is how he broke down individual validation rules into small, re-usable helper predicate functions (`is_null`, `is_int`). One thing I would do differently next time is perform code reviews directly on pull request line diffs sooner rather than reviewing bulk commits at the end.

---

## 6. Declaration

- [x] Both of us can explain every line in this repository.
- [x] AI assistants used for explanation only, not to generate our implementation or our tests.

**If you used an AI assistant, say what you asked and what you did with the answer:**
We asked an AI assistant to clarify Git terminal output regarding detached HEAD states and tracking remote branches, and to explain the difference between `.strip()` and `.rstrip("\r\n")` when parsing CSV line endings in Python. We used these explanations to resolve local branch setup issues and refine our line-parsing logic.

---

## Running this project

```bash
pytest -v                              # all tests
pytest tests/test_provided.py -v       # the given suite
pytest tests/test_yours.py -v          # your suite
python tools/check_collaboration.py    # your Part C report