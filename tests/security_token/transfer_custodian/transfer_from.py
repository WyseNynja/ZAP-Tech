#!/usr/bin/python3

from brownie import *
from scripts.deployment import main


def setup():
    main(SecurityToken)
    global token, issuer, cust
    token = SecurityToken[0]
    issuer = IssuingEntity[0]
    cust = OwnedCustodian.deploy(a[0], [a[0]], 1, {'from': a[0]})
    issuer.addCustodian(cust, {'from': a[0]})
    token.mint(issuer, 100000, {'from': a[0]})


def issuer_txfrom():
    '''Issuer transferFrom custodian'''
    token.transfer(a[1], 10000, {'from': a[0]})
    token.transfer(cust, 10000, {'from': a[1]})
    token.transferFrom(cust, a[1], 5000, {'from': a[0]})
    check.equal(token.balanceOf(a[1]), 5000)
    check.equal(token.balanceOf(cust), 5000)
    check.equal(token.custodianBalanceOf(a[1], cust), 5000)

def investor_txfrom():
    '''Investor transferFrom custodian'''
    token.transfer(a[1], 10000, {'from': a[0]})
    token.transfer(cust, 10000, {'from': a[1]})
    check.reverts(
        token.transferFrom,
        (cust, a[1], 5000, {'from': a[1]}),
        "Insufficient allowance"
    )
    check.reverts(
        token.transferFrom,
        (cust, a[1], 5000, {'from': a[2]}),
        "Insufficient allowance"
    )