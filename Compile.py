import json
from solcx import compile_standard
import os


def compile_sol(script_path):
    script_name = os.path.basename(script_path)
    with open(script_path, "r") as file:
        contact_list_file = file.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {script_name: {"content": contact_list_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.0",
    )
    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)
    return compiled_sol

