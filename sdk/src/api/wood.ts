import {NeoInterface} from "../interface";
import Neon, { sc } from "@cityofzion/neon-js";
import {wallet} from "@cityofzion/neon-core";

export class Wood {

  static async symbol(node: string, networkMagic: number, contractHash: string): Promise<string> {
    const method = "symbol"

    const res = await NeoInterface.TestInvoke(node, networkMagic, contractHash, method, [] )
    if (res === undefined || res.length === 0) {
      throw new Error("unrecognized response")
    }
    return Neon.u.HexString.fromBase64(res[0].value as string).toAscii()
  }

  static async decimals(node: string, networkMagic: number, contractHash: string): Promise<number> {
    const method = "decimals"

    const res = await NeoInterface.TestInvoke(node, networkMagic, contractHash, method, [] )
    if (res === undefined || res.length === 0) {
      throw new Error("unrecognized response")
    }
    return parseInt(res[0].value as string)
  }

  static async totalSupply(node: string, networkMagic: number, contractHash: string): Promise<number> {
    const method = "totalSupply"

    const res = await NeoInterface.TestInvoke(node, networkMagic, contractHash, method, [] )
    if (res === undefined || res.length === 0) {
      throw new Error("unrecognized response")
    }
    return parseInt(res[0].value as string)
  }

  static async balanceOf(node: string, networkMagic: number, contractHash: string, address: string): Promise<any> {
    const method = "balanceOf"
    const params = [
      sc.ContractParam.hash160(address)
    ]

    const res = await NeoInterface.TestInvoke(node, networkMagic, contractHash, method, params )
    if (res === undefined || res.length === 0) {
      throw new Error("unrecognized response")
    }
    return parseInt(res[0].value as string)
  }

  static async transfer(node: string, networkMagic: number, contractHash: string, fromAddress: string, toAddress: string, amount: number, account: wallet.Account, data?: any): Promise<any> {
    const method = "transfer"
    const params = [
      sc.ContractParam.hash160(fromAddress),
      sc.ContractParam.hash160(toAddress),
      amount,
      data
    ]

    const res = await NeoInterface.publishInvoke(node, networkMagic, contractHash, method, params, account )
    return res
  }

  static async mint(node: string, networkMagic: number, contractHash: string, address: string, amount: number, account: wallet.Account): Promise<any> {
    const method = "mint"

    const params = [
      sc.ContractParam.hash160(address),
      amount
    ]
    const res = await NeoInterface.publishInvoke(node, networkMagic, contractHash, method, params, account )
    return res
  }

  static async burn(node: string, networkMagic: number, contractHash: string, address: string, amount: number, account: wallet.Account): Promise<any> {
    const method = "burn"
    const params = [
      sc.ContractParam.hash160(address),
      amount
    ]

    const res = await NeoInterface.publishInvoke(node, networkMagic, contractHash, method, params, account )
    return res
  }

  static async onNEP17Payment(node: string, networkMagic: number, contractHash: string, address: string, amount: number, data: any, account: wallet.Account): Promise<any> {
    const method = "onNEP17Payment"
    const params = [
      sc.ContractParam.hash160(address),
      amount,
      data
    ]

    const res = await NeoInterface.publishInvoke(node, networkMagic, contractHash, method, params, account )
    return res
  }
}