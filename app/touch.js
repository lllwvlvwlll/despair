const sdk = require("../sdk/dist")
const neon = require("@cityofzion/neon-js")
global.TextEncoder = require("util").TextEncoder;

const hash = {
    "despair": "0xd006a7a989d2c217ec278827ce408115708fff76",
    "wood": "0xcfa09b19f723d9696726912a306362c3212a01c4",
    //"gold": "0x8050dc0e1508bfc11d8bc6b3e6a6812d2deba9a8",
    //"water": "0x93fdba09fa40a38894bc18730af3a18fa10517ea",
    //"stone": "0x3c1c7002b8fcd57ff43c8b8cf0f62980e2483169",
    //"wheat": "0x41aaee3b5a5169b5daa9f1f21bdb889ef47a010e"
}



const TEST_ACCOUNTA = new neon.wallet.Account("0799e612c9ee2bc8a7eab43ba5154caf5a26f27ded2525719a7c31e6d3f13ce0")
const TEST_ACCOUNTB = new neon.wallet.Account("46f20119aae10ad7eb6d4a8e057fca25cfaf2223ac7ed5b1358c56de7b88e314")
const NODE = "http://localhost:50012"
const NETWORK_MAGIC = 827601742

async function Main()
{
    const config = {
        networkMagic: NETWORK_MAGIC, // Replace with your preferred network (Private network number, MainNet, TestNet)
        rpcAddress: NODE, // the RPC end point to use for retrieving information and sending the transaction to the network
        account: TEST_ACCOUNTA,
    };


    /*
    console.log("//////////////////WOOD///////////////////////")

    let res = await sdk.Wood.symbol(NODE, NETWORK_MAGIC, hash.wood)
    console.log("symbol: ", res)

    res = await sdk.Wood.decimals(NODE, NETWORK_MAGIC, hash.wood)
    console.log("decimals: ", res)

    res = await sdk.Wood.totalSupply(NODE, NETWORK_MAGIC, hash.wood)
    console.log("total supply: ", res)

    res = await sdk.Wood.mint(NODE, NETWORK_MAGIC, hash.wood, TEST_ACCOUNTA.address, 100, TEST_ACCOUNTA)
    console.log("mint: ", res)


    res = await sdk.Wood.balanceOf(NODE, NETWORK_MAGIC, hash.wood, TEST_ACCOUNTA.address)
    console.log("balanceOf: ", res)
    */

    console.log("//////////////////DESPAIR///////////////////////")

    res = await sdk.Despair.symbol(NODE, NETWORK_MAGIC, hash.despair)
    console.log("symbol: ", res)

    res = await sdk.Despair.decimals(NODE, NETWORK_MAGIC, hash.despair)
    console.log("decimals: ", res)


    res = await sdk.Despair.createLand(NODE, NETWORK_MAGIC, hash.despair, TEST_ACCOUNTA.address, TEST_ACCOUNTA)
    console.log("createA: ", res)


    setTimeout(async () => {
        res = await sdk.Despair.claimBounty(NODE, NETWORK_MAGIC, hash.despair, "i_1", "wood", TEST_ACCOUNTA)
        console.log("claim wood: ", res)

        res = await sdk.Despair.claimBounty(NODE, NETWORK_MAGIC, hash.despair, "i_1", "wheat", TEST_ACCOUNTA)
        console.log("claim wheat: ", res)
    }, 10000)

    //res = await sdk.Despair.createLand(NODE, NETWORK_MAGIC, hash.despair, TEST_ACCOUNTB.address, TEST_ACCOUNTB)
    //console.log("createB: ", res)

    setInterval( async () => {
        /*
        res = await sdk.Despair.totalSupply(NODE, NETWORK_MAGIC, hash.despair)
        console.log("totalSupply: ", res)

        res = await sdk.Despair.getLand(NODE, NETWORK_MAGIC, hash.despair, "i_1")
        console.log("getLand: ", res.wheat, res.wood)
        */
        res = await sdk.Despair.getUnclaimed(NODE, NETWORK_MAGIC, hash.despair, "i_1", "wood")
        console.log("unclaimed_wood: ", res)

        res = await sdk.Despair.getUnclaimed(NODE, NETWORK_MAGIC, hash.despair, "i_1", "wheat")
        console.log("unclaimed_wheat: ", res)

        res = await sdk.Wood.balanceOf(NODE, NETWORK_MAGIC, hash.wood, TEST_ACCOUNTA.address)
        console.log("balanceOf wood: ", res)

    }, 2000)

    //res = await sdk.Despair.getLand(NODE, NETWORK_MAGIC, hash.despair, TEST_ACCOUNTB.address)
    //console.log("getLand: ", res)



    // = await sdk.Despair.tokensOf(NODE, NETWORK_MAGIC, hash.despair,TEST_ACCOUNTA.address)
    //console.log("getLand: ", res)

    //res = await sdk.Despair.getLand(NODE, NETWORK_MAGIC, hash.despair,"i_2")
    //console.log("getLand: ", res)

    //res = await sdk.Despair.getLand(NODE, NETWORK_MAGIC, hash.despair,"i_3")
    //console.log("getLand: ", res)


}
Main()