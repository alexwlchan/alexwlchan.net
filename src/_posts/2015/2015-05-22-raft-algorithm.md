---
layout: post
date: 2015-05-22 17:40:00 +0000
link: http://thesecretlivesofdata.com/raft/
summary: A visualisation of the Raft consensus algorithm.
title: <em>The Secret Lives of Data</em>, a visualisation of the Raft algorithm
category: Link posts
index:
  exclude: true
---

One of the big problems in computer science is [distributed consensus](https://en.wikipedia.org/wiki/Consensus_(computer_science)). This is the problem of getting a set of nodes in a network (or distributed system) to agree on something: perhaps a value, an action, or a record of history. Some of the nodes in this system will be faulty, and drop messages, so you need to be able to work around that as well. This turns out to be very difficult to solve.

There are two commonly-used algorithms for solving this problem: [Paxos](https://en.wikipedia.org/wiki/Paxos_(computer_science)) and [Raft](https://en.wikipedia.org/wiki/Raft_(computer_science)). Both have been mathematically proven to work to solve the consensus problem.

As part of my day job ([Project Calico](http://www.projectcalico.org/)), we use [etcd](https://github.com/coreos/etcd) as a distributed database layer, which implements the Raft algorithm for consensus. Since Raft was explicitly designed to be understandable (as opposed to Paxos's reputation for inscrutability), I thought it was worth trying to understand how it works.

I came across this visualisation, which explains how the Raft algorithm works. It takes you from the basics of the consensus problem, through the design of the Raft algorithm and explains how it copes when the network starts to fail. I found it really interesting, and I think it's well worth a read.
