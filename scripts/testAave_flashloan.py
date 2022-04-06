from brownie import accounts, Contract, interface, config, network, TestAaveFlashLoan


def main():
    active_network = network.show_active()
    ADDRESS_PROVIDER = "0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5"
    testAaveFlashloan = TestAaveFlashLoan.deploy(
        ADDRESS_PROVIDER, {"from": accounts[0]})

    USDC = config["networks"][active_network]["USDC"]
    USDC_WHALE = config["networks"][active_network]["USDC_WHALE"]

    WHALE = USDC_WHALE
    TOKEN_BORROW = USDC
    token = Contract.from_abi("USDC", TOKEN_BORROW,
                              interface.IERC20.abi)
    DECIMALS = token.decimals()
    FUND_AMOUNT = 2000*10**DECIMALS  # 2000 USDC
    BORROW_AMOUNT = 1000*10**DECIMALS  # borrow 1000 USDC

    print(
        f"Initial, testAaveFlashloan : {token.balanceOf(testAaveFlashloan)/10**DECIMALS} {token.symbol()}")

    # send enough token to cover fee
    bal = token.balanceOf(WHALE)
    print(f"Balance of WHALE is {bal/10**DECIMALS} {token.symbol()}")
    assert bal > FUND_AMOUNT
    print(
        f"Funding the testAaveFlashloan contract with {FUND_AMOUNT/10**DECIMALS} {token.symbol()}")
    token.transfer(testAaveFlashloan.address, FUND_AMOUNT, {"from": WHALE})
    print(
        f"After funding, testAaveFlashloan : {token.balanceOf(testAaveFlashloan)/10**DECIMALS} {token.symbol()}")

    print(
        f"Flashloan {BORROW_AMOUNT/10**DECIMALS} {token.symbol()} from WHALE")

    tx = testAaveFlashloan.testFlashLoan(
        token.address, BORROW_AMOUNT, {"from": WHALE})
    tx.wait(1)
    print(
        f"After Flashloan, testAaveFlashloan : {token.balanceOf(testAaveFlashloan)/10**DECIMALS} {token.symbol()}")
    print(tx.events["Log"][0]["message"], tx.events["Log"][0]["val"])
    print(tx.events["Log"][1]["message"], tx.events["Log"][1]["val"])
