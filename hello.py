def main() -> int:
    """
    __C_CODE__
    printf("C:Hello from py2mcu!\n");
    return 0;
    """
    print("Hello from py2mcu!")
    return 0

if __name__ == "__main__":
    main()
