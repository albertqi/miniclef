import os


def main() -> None:
    """Consolidate all SuperCollider code in the 'synths' folder into a single file."""

    with open("out.scd", "w") as out:
        out.write("(\n")
        dir = "synths"
        files = os.listdir(dir)
        for file in files:
            with open(f"{dir}/{file}") as f:
                # Replace 'add' with 'writeDefFile'.
                txt = f.read()
                replace_txt = f'writeDefFile("{os.getcwd()}/compiled")'
                new_txt = txt[::-1].replace("add"[::-1], replace_txt[::-1], 1)[::-1]
                out.write(new_txt + "\n")
        out.write(")\n")

    print("Done!")


if __name__ == "__main__":
    main()
