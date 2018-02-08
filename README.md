# eth资金流向查看   api from py-etherscan-api module



以太坊地址 账本追踪
1.给定一个或多个节点开始爬， 可能需要爬当前页， 还要下载csv分析（直接通过api来下载数据）， 爬过的tx交易都打上标记，存入数据库中
2.爬完后会把数据存到本地
3.出入越大的节点，自身图片越大，代表大户

4.可以给自己想要查的一笔资金或者一笔交易tx，打上标记，在图示上标一个颜色，展示流向
5.图片可以参考天眼里分析公司的那个





EtherScan.io API python bindings

## Description
This module is written as an effort to provide python bindings to the EtherScan.io API, which can be found at:
https://etherscan.io/apis
In order to use this, you must attain an Etherscan user account, and generate an API key.

In order to use the API, you must provide an API key at runtime, which can be found at the Etherscan.io API website.
If you'd like to use the provided examples without altering them, then the JSON file `api_key.json` must be stored in
the base directory.  Its format is as follows:

    { "key" : "YourApiKeyToken" }

with `YourApiKeyToken` is your provided API key token from EtherScan.io

## Installation
To install the package to your computer, simply run the following command in the base directory:

    python setup.py install

## Available bindings
Currently, only the following Etherscan.io API modules are available:

- accounts
- stats
- tokens

The remaining available modules provided by Etherscan.io will be added shortly

## Examples
All possible calls have an associated example file in the examples folder to show how to call the binding

These of course will be fleshed out with more details and explanation in time

Jupyter notebooks area also included in each directory to show all examples

## TODO:

- Package and submit to PyPI
- Add the following modules:
    - event logs
    - geth proxy
    - websockets
- Add robust documentation
- Add unit test suite
- Add request throttling based on Etherscan's suggestions


## Holla at ya' boy
BTC: 16Ny72US78VEjL5GUinSAavDwARb8dXWKG

ETH: 0x5E8047fc033499BD5d8C463ADb29f10f11165ed0
