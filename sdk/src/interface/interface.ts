import Neon, {rpc, sc, tx} from '@cityofzion/neon-js'
import StackItemJson from '@cityofzion/neon-core'

export class NeoInterface {

  static async TestInvoke(node: string, contractHash: string, method: string, params: any[]): Promise< StackItemJson.sc.StackItemJson[] | undefined> {

    const res = await new rpc.RPCClient(node).invokeFunction(
      contractHash,
      method,
      params
    )

    return res.stack
  }


  /*

  static  async publishInvoke(): {

  }

  */

}