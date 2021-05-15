const sdk = require("../sdk/dist")

const SCRIPTHASH = '0x8c6651015262320fc6457aeb7a50e9a5a1a4a1dd'
const NODE = "http://localhost:50012"

async function Main()
{
    const res = await sdk.Despair.hello(NODE, SCRIPTHASH)
    console.log(res)
}
Main()