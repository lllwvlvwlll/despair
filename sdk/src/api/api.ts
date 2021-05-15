import { NeoInterface } from '../interface'
import Neon from "@cityofzion/neon-js";

export class Despair {
  /**
   * Initializes the smart contract after deployment.
   * @param node
   * @param contractHash
   */
  static async init(node: string, contractHash: string): Promise<any> {
    const method = "init"

    const res = await NeoInterface.TestInvoke(node, contractHash, method, [] )

    return res
  }

  /**
   * Executes the hello method on the smart contract.
   * @param node the rpc endpoint to target (http://localhost:50012"
   * @param contractHash (the script hash of the contract)
   */
  static async hello(node: string, contractHash: string): Promise<string> {
    const method = "hello"

    const res = await NeoInterface.TestInvoke(node, contractHash, method, [] )
    if (res === undefined) {
      throw new Error("unrecognized response")
    }
    const value = Neon.u.HexString.fromBase64(res[0].value as string).toAscii()
    return value
  }
}