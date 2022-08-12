# Framework for the predcition API

Contents:

* [Summary](#summary)
  * [Issue](#issue)
  * [Decision](#decision)
  * [Status](#status)
* [Details](#details)
  * [Assumptions](#assumptions)
  * [Constraints](#constraints)
  * [Positions](#positions)
  * [Argument](#argument)
* [Notes](#notes)


## Summary


### Issue

We need to choose a framework for building the predection API.


### Decision

So far, I am choosing FastAPI.


### Status

Open. 


## Details
Studying it so far.


### Assumptions
Studying it so far.


### Constraints
Studying it so far.



### Positions

So far, I considered these frameworks:

  * Django

  * Flask

  * FastAPI


### Argument

Summary per framework:

  * Flask: enables easily scalable applications. Another advantage is that Flask has a great flexibility. are easily and extensively scalable. Flask community is well established. well equipped to handle common security concerns like CSRF, XSS or JSON security. as cons, lack of support for asynchronicity and that Flask uses third-party modules, which might have a negative effect on security.


  * Django: make it easy to develop complex database-driven websites. inflexible MVT design. great ORM. lots of out-of-the-box features.

  * FastAPI: has high performance, and easily supports concurrency. It offers a simple and easy-to-use dependency injection system. Inbuilt data validation is another benefit to take into consideration. As cons, lack of inbuilt security system and small community of developers.

Since the scope of the prediction API is short for now, and the expected growth is in volume, not in new features, FastAPI seems to be the best option. We won't manage users, access and permissions.

FastAPI has a built-in background task processor and enables assynchronous processing.

The down side is regarding security, but for the challenge purpose, and api_token scheme should be enough.


## Notes

[2022-08-11] FastAPI is the best candidate so far.