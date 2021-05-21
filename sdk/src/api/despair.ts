import { NeoInterface } from '../interface'
import Neon, {sc, u} from "@cityofzion/neon-js";
import {wallet} from "@cityofzion/neon-core";
import Dict = NodeJS.Dict;

export class Despair {

  static async symbol(node: string, networkMagic: number, contractHash: string): Promise<string> {
    const method = "symbol"

    const res = await NeoInterface.TestInvoke(node, networkMagic, contractHash, method, [] )
    if (res === undefined) {
      throw new Error("unrecognized response")
    }
    return Neon.u.HexString.fromBase64(res[0].value as string).toAscii()
  }

  static async decimals(node: string, networkMagic: number, contractHash: string): Promise<number> {
    const method = "decimals"

    const res = await NeoInterface.TestInvoke(node, networkMagic, contractHash, method, [] )
    if (res === undefined) {
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

  static async getLand(node: string, networkMagic: number, contractHash: string, address: string): Promise<{ [key: string]: any } | undefined> {
    const method = "land_get"
    const params = [
      sc.ContractParam.hash160(address),
      ]

    const res = await NeoInterface.TestInvoke(node, networkMagic, contractHash, method, params)
    if (res === undefined || res.length === 0 || res[0].value === undefined) {
      return undefined
    }

    let land: { [key: string]: any } = {};
    (res[0].value as any[]).forEach( (d, i) => {
      let key = Neon.u.HexString.fromBase64(d.key.value as string).toAscii()

      if (d.value.type == "Integer") {
        land[key] = parseInt(d.value.value)
      } else if (d.value.type = "ByteString") {
        land[key] = Neon.u.HexString.fromBase64(d.value.value as string).toAscii()
      }
    })

    return land
  }

  static async createLand(node: string, networkMagic: number, contractHash: string, address: string, account: wallet.Account): Promise<any> {
    const method = "create_land"

    const params = [
      sc.ContractParam.hash160(address),
    ]


    return await NeoInterface.publishInvoke(node, networkMagic, contractHash, method, params, account )

  }

}