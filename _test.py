import mfs


def main():
    inputprompt = input(": ")
    inputprompt += " Відповідь має бути Українською мовою."
    output = mfs.you(inputprompt)
    print(output)


if __name__ == "__main__":
    main()
