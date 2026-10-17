# K2 development set: originals of RP:P and Many Labs

Bibliographic records only (title, authors, journal, volume, pages, DOI, how
each DOI was verified). **No replication outcomes**, by design: PREREG-K2-DRAFT
§7.1 consequence 5 forbids using development-set outcomes to shape the rubric.

| File | Built by | From |
|---|---|---|
| `devset_rpp.csv`, `devset_rpp_summary.json` | `../k2_devset_rpp.py` | `CenterForOpenScience/rpp`, `data_allformats/RPPdataConverted.csv`, sha256 `e753eae64a65015069217aa68effc85cd797fa2f9fc0958cbbf463dc3d505ddb`, fetched 2026-10-17 |
| `devset_ml.csv`, `devset_ml_summary.json` | `../k2_devset_ml.py` | `ManyLabsOpenScience/ManyLabs1` `ML_Original_ES95CI.xls` (sha256 in the summary); `ManyLabsOpenScience/ManyLabs2` folder names under `OSFdata/`; the ML4 repository README (`raklein/ml4`); the Many Labs articles' Crossref reference lists |

Both scripts ran on Atlas. Every DOI was checked against Crossref (or PubMed for
ML4); the `doi_status` column says how. A row that could not be verified has an
empty DOI and says why. Nothing was filled from memory.

**Licenses.** The RP:P GitHub mirror declares no license; ML1's data folder
says "Data released under CC0 license". These files hold bibliographic facts
about published articles, not the projects' data. Confirm the RP:P license on
OSF before sealing (registration §3, requirement 4).

**Unit.** Rubric development codes the original article. Some articles appear
more than once (see the summaries' `shared_doi` and `ml_rpp_overlap`); the
seeded draw is over distinct DOIs.
