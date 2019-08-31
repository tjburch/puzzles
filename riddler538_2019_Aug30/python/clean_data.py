import csv
datadir = "/Users/tburch/Documents/github/puzzles/riddler538_2019_Aug30/data/"
files = [datadir+"castle-solutions.csv", datadir+"castle-solutions-2.csv", datadir+"castle-solutions-3.csv"]
fout = open(datadir+"castle-solutions-clean.csv","w+")

def clean_file(filename):
    fout = open(filename.replace(".csv","-clean.csv"),"w+")

    with open(filename,"r+") as f:
        fout.write(
            "Castle 1" + "," +
            "Castle 2" + "," +
            "Castle 3" + "," +
            "Castle 4" + "," +
            "Castle 5" + "," +
            "Castle 6" + "," +
            "Castle 7" + "," +
            "Castle 8" + "," +
            "Castle 9" + "," +
            "Castle 10" + "\n"
        )


        reader = csv.DictReader(f)    
        for row in reader:
            fout.write(
                row["Castle 1"] + "," +
                row["Castle 2"] + "," +
                row["Castle 3"] + "," +
                row["Castle 4"] + "," +
                row["Castle 5"] + "," +
                row["Castle 6"] + "," +
                row["Castle 7"] + "," +
                row["Castle 8"] + "," +
                row["Castle 9"] + "," +
                row["Castle 10"] + "\n"
            )

for f in files:
    clean_file(f)

