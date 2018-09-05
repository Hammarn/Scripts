#!/usr/bin/env python


if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Make a scatter plot of FPKM counts between conditions")
    parser.add_argument("-s", "--summary", dest="summary", action='store_true',
help="Input files are summary FPKM files.")

    args = vars(parser.parse_args())
