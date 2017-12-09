
RT Query
========

.. image:: https://travis-ci.org/tarvitz/rtquery.svg?branch=master
    :target: https://travis-ci.org/tarvitz/rtquery

.. image:: https://coveralls.io/repos/github/tarvitz/rtquery/badge.svg?branch=master
  :target: https://coveralls.io/github/tarvitz/rtquery?branch=master

.. image:: https://badge.fury.io/py/rtquery.svg
    :target: https://badge.fury.io/py/rtquery

.. contents::
    :local:
    :depth: 2

Abstract
--------
Simplifies query interface for |rt_tracker|_'s rest-api lib |rt_lib|_.
Main query interface has been take from |django|_ project

Requirements
------------

- Python 3.4+
- |rt_lib|_ (it's not dependency itself, but it uses in examples)

Usage
-----

.. code-block:: python

    import rt

    client = rt.Rt('http://localhost/rt/REST/1.0/',
                   basic_auth=('user', 'password'))
    assert client.login()
    #: rt filtering does not support `in` operation, so interface looks similar
    #: to django querying, but it sticks to its limits.
    query = Q(Subject__contains='[improvements]') | Q(Subject__contains='[enhancements]')
    query &= Q(Queue='development', Status='sprint', Owner='User',
               Priority__gt=80)
    result = client.search(Queue=rt.ALL_QUEUES, raw_query=query.resolve())
    print(result)
    [{
        "id": "ticket/471147",
        "Queue": "development",
        "Owner": "User",
        "Creator": "User",
        "Subject": "[improvements] Implement Requests Tracker simple querying",
        "Status": "sprint",
        "Priority": "99",
        "InitialPriority": "40",
        "FinalPriority": "40",
        "Requestors": [
            "user@example.org.fake"
        ],
        "Created": "Thu Nov 02 19:26:40 2017",
        "Starts": "Not set",
        "Started": "Thu Nov 02 19:27:12 2017",
        "Due": "Not set",
        "Resolved": "Not set",
        "Told": "Not set",
        "LastUpdated": "Thu Nov 09 17:20:33 2017",
        "TimeEstimated": "180 minutes",
        "TimeWorked": "0",
        "TimeLeft": "0",
        "CF.{Tags}": "extra",
        "CF.{Code Review}": "",
        "CF.{Difficulty}": ""
    }]

Extra functionality
-------------------
In addition to existent ``rtquery.Q`` you can also try to use ``utils.query``
builder which is simple dsl to make ``Q`` objects from user input (argument parser for example)

.. code-block:: python

    from rtquery.utils import query
    qset = query("Queue = development & Status = sprint & Owner ~ user")
    result = client.search(Queue=rt.ALL_QUEUES, raw_query=query.resolve())
    # ...

.. references

.. |rt_tracker| replace:: Request Tracker
.. _rt_tracker: https://bestpractical.com/request-tracker
.. |rt_lib| replace:: RT Library
.. _rt_lib: https://github.com/CZ-NIC/python-rt
.. |django| replace:: Django Framework
.. _django: https://www.djangoproject.com/
