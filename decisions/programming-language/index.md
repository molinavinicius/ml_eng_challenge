# Programming languages

Contents:

* [Summary](#summary)
  * [Issue](#issue)
  * [Decision](#decision)
  * [Status](#status)
* [Details](#details)
  * [Assumptions](#assumptions)
  * [Constraints](#constraints)
  * [Implications](#implications)
* [Related](#related)
  * [Related decisions](#related-decisions)
* [Notes](#notes)


## Summary


### Issue

I need to choose programming languages for the pipeline. I have two major needs: a pipeline, responsible for tasks such as pre-processing and training a model, and a prediction API. It is not a strong requirement, but doing both in the same programming language can make it easier.


### Decision

I am choosing Python for both.


### Status

Decided.


## Details


### Assumptions

The data pipeline will have to perform tasks such as:

  *   Data extraction;
  *   Data validation;
  *   Data preparation;
  *   Model training;
  *   Model evaluation,
  *   and Model validation.

While the prediction API will:

  *   Read the serialized model (artifact) storaged at the model registry;
  *   Check if the incoming data is valid;
  *   Use the model to make a prediction;
  *   Return a HTTP response.

The API is likely to evolve to allow monitoring purposes and logging. We also need fast responses.

### Constraints

The choice has to consider languages that are open source and they do not depend on a particular cloud vendor. And also that can be easily tested locally and do not
need big infrastructure (for example, a cluster) to work.


### Implications

Choosing the same language for both parts, we can start with a small team that is self-sufficient to build and maintain the entire pipeline (from preprocessing to prediction).

Although other languages could be chosen for build the prediction API, Python is great for all the data preparation process. 

Furthermore, Jupyter Notebook (the status quo) are usually written with Python, so we can reuse lots of code with this choice.


## Related


### Related decisions

We will aim toward ecosystem choices that align with Python.

The `framework-prediction-api` is fully impacted by this decision.


## Notes

[2022-08-11] Decision made. Python was the programming language of choice.