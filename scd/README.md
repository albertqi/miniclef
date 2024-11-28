# Compiling SCD Files

The `synths` and `effects` folders contain SuperCollider code. This code is meant to be compiled into `scsyndef` files so that `scsynth` can load the compiled files. Compiled files are located in the `compiled` folder.

The `process.py` file consolidates all of the SuperCollider code in the `synths` and `effects` folders into one large file `out.scd`. This file can then be run in SuperCollider in order to generate the appropriate compiled files in the `compiled` folder. That is, in order to generate compiled `scsyndef` files, you should:

1. Run the `process.py` file.
2. Open the generated `out.scd` file in SuperCollider.
3. Run the file in SuperCollider, and voila!
