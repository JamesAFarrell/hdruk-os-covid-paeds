from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

# Import json and datetime module
import json
import datetime

############
# Codelist #
############

# Import Codelists
from codelists import *

gp_codelist = snomed_specimen

####################
# Study Definition #
####################

# Import global-variables.json
with open("./analysis/global_variables.json") as f:
    gbl_vars = json.load(f)

# Define study date variables
start_date = gbl_vars["start_date"]
end_date   = gbl_vars["end_date"]

# Number of hospital admissions, outpatient appointments, GP interactions, covid tests to query
n_gp      = gbl_vars["n_gp"]

# Study definition
study = StudyDefinition(

    index_date=start_date,

    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    # Study population: Alive and registered as of study start, registered at study end or died during study, age between 1 and 18 years
    population=patients.satisfying(
        """
        (NOT died_before_start_date) AND registered_at_start_date
        AND (registered_at_end_date OR died_during_study)
        AND (age_on_start_date > 1) AND (age_on_start_date < 18)
        AND (gp_weekly_count > 0)
        """,
        registered_at_start_date=patients.registered_as_of(
            start_date,
        ),
        registered_at_end_date=patients.registered_as_of(
            end_date,
        ),
        died_before_start_date=patients.died_from_any_cause(
            on_or_before=start_date,
            returning="binary_flag",
        ),
        died_during_study=patients.died_from_any_cause(
            between=[start_date, end_date],
            returning="binary_flag",
        ),
        age_on_start_date=patients.age_as_of(
            start_date,
        ),
        gp_weekly_count=patients.with_these_clinical_events(
            codelist = gp_codelist,
            returning="number_of_matches_in_period",
            between=["index_date", "index_date + 6 days"],
            return_expectations={
                "int": {"distribution": "poisson", "mean": 1},
                "incidence": 1,
            },
        ),
    ),

    ##############
    # GP Contact #
    ##############

    gp_count_1=patients.with_these_clinical_events(
        codelist = gp_codelist,
        returning="number_of_matches_in_period",
        between=["index_date", "index_date"],
        return_expectations={
            "int": {"distribution": "poisson", "mean": 0.1},
            "incidence": 1,
        },
    ),

    gp_count_2=patients.with_these_clinical_events(
        codelist = gp_codelist,
        returning="number_of_matches_in_period",
        between=["index_date + 1 day", "index_date + 1 day"],
        return_expectations={
            "int": {"distribution": "poisson", "mean": 0.1},
            "incidence": 1,
        },
    ),

    gp_count_3=patients.with_these_clinical_events(
        codelist = gp_codelist,
        returning="number_of_matches_in_period",
        between=["index_date + 2 day", "index_date + 2 day"],
        return_expectations={
            "int": {"distribution": "poisson", "mean": 0.1},
            "incidence": 1,
        },
    ),

    gp_count_4=patients.with_these_clinical_events(
        codelist = gp_codelist,
        returning="number_of_matches_in_period",
        between=["index_date + 3 day", "index_date + 3 day"],
        return_expectations={
            "int": {"distribution": "poisson", "mean": 0.1},
            "incidence": 1,
        },
    ),

    gp_count_5=patients.with_these_clinical_events(
        codelist = gp_codelist,
        returning="number_of_matches_in_period",
        between=["index_date + 4 day", "index_date + 4 day"],
        return_expectations={
            "int": {"distribution": "poisson", "mean": 0.1},
            "incidence": 1,
        },
    ),

    gp_count_6=patients.with_these_clinical_events(
        codelist = gp_codelist,
        returning="number_of_matches_in_period",
        between=["index_date + 5 day", "index_date + 5 day"],
        return_expectations={
            "int": {"distribution": "poisson", "mean": 0.1},
            "incidence": 1,
        },
    ),

    gp_count_7=patients.with_these_clinical_events(
        codelist = gp_codelist,
        returning="number_of_matches_in_period",
        between=["index_date + 6 day", "index_date + 6 day"],
        return_expectations={
            "int": {"distribution": "poisson", "mean": 0.1},
            "incidence": 1,
        },
    ),

)
