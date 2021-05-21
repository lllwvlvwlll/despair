import Neon, {rpc, u, api, sc, tx} from '@cityofzion/neon-js'
import StackItemJson, { wallet } from '@cityofzion/neon-core'
const fs = require("fs").promises;

export class NeoInterface {

  static async TestInvoke(rpcAddress: string, networkMagic: number, scriptHash: string, operation: string, args: any[]): Promise< StackItemJson.sc.StackItemJson[] | undefined> {
    const contract = new Neon.experimental.SmartContract(
      Neon.u.HexString.fromHex(scriptHash),
      {
        networkMagic,
        rpcAddress,
      }
    );
    let res = await contract.testInvoke(operation, args)

    return res.stack
  }

  static async publishInvoke(rpcAddress: string, networkMagic: number, scriptHash: string, operation: string, args: any[], account: wallet.Account): Promise< string | undefined> {

    const contract = new Neon.experimental.SmartContract(
      Neon.u.HexString.fromHex(scriptHash),
      {
        networkMagic,
        rpcAddress,
        account,
        //systemFeeOverride: u.BigInteger.fromDecimal(1, 0)
      }
    );

    let result
    try {
      result = await contract.invoke(operation, args)
    } catch (e) {
      console.log("errored here")
      console.log(e)
    }

    return result
  }


}