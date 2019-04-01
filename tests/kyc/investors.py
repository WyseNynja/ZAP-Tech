#!/usr/bin/python3

from brownie import *
from scripts.deployment import main


def setup():
    config['test']['always_transact'] = False
    global kyc, issuer, auth_id
    kyc = a[0].deploy(KYCRegistrar, [a[0]], 1)
    issuer = a[0].deploy(IssuingEntity, [a[0]], 1)
    #token = accounts[0].deploy(token_contract, issuer, "Test NFT", "NFT", 1000000)
    #issuer.addToken(token, {'from': accounts[0]})
    issuer.setRegistrar(kyc, True, {'from': a[0]})
    kyc.addAuthority((a[-1],a[-2]), [], 1, {'from': a[0]})
    auth_id = kyc.getAuthorityID(a[-1])


# updateInvestor
# setInvestorRestriction
# setInvestorAuthority

def add_investor_country_zero():
    '''add investor - country 0'''
    check.reverts(
        kyc.addInvestor,
        ("0x1234", 0, 1, 1, 9999999999, (a[1], a[2]), {'from': a[0]}),
        "dev: country 0"
    )

def add_investor_rating_zero():
    '''add investor - rating 0'''
    check.reverts(
        kyc.addInvestor,
        ("0x1234", 1, 1, 0, 9999999999, (a[1], a[2]), {'from': a[0]}),
        "dev: rating"
    )

def add_investor_authority_id():
    '''add investor - known authority ID'''
    check.reverts(
        kyc.addInvestor,
        (auth_id, 1, 1, 1, 9999999999, (a[1], a[2]), {'from': a[0]}),
        "dev: authority ID"
    )


def add_investor_investor_id():
    '''add investor - known investor ID'''
    kyc.addInvestor("0x1234", 1, 1, 1, 9999999999, (a[1], a[2]), {'from': a[0]})
    check.reverts(
        kyc.addInvestor,
        ("0x1234", 1, 1, 1, 9999999999, (a[3],), {'from': a[0]}),
        "dev: investor ID"
    )


def add_investor_authority_country():
    '''add investor - authority country permission'''
    check.reverts(
        kyc.addInvestor,
        ("0x1234", 1, 1, 1, 9999999999, (a[3],), {'from': a[-1]}),
        "dev: country"
    )
    kyc.setAuthorityCountries(auth_id, (1,), True, {'from': a[0]})
    kyc.addInvestor("0x1234", 1, 1, 1, 9999999999, (a[3],), {'from': a[-1]})
    check.reverts(
        kyc.addInvestor,
        ("0x5678", 2, 1, 1, 9999999999, (a[4],), {'from': a[-1]}),
        "dev: country"
    )
    kyc.setAuthorityCountries(auth_id, (1,), False, {'from': a[0]})
    check.reverts(
        kyc.addInvestor,
        ("0x5678", 1, 1, 1, 9999999999, (a[4],), {'from': a[-1]}),
        "dev: country"
    )


def update_investor_unknown_id():
    '''update investor - unknown ID'''
    check.reverts(
        kyc.updateInvestor,
        ("0x1234", 1, 1, 9999999999, {'from': a[0]}),
        "dev: unknown ID"
    )
    check.reverts(
        kyc.updateInvestor,
        (auth_id, 1, 1, 9999999999, {'from': a[0]}),
        "dev: unknown ID"
    )