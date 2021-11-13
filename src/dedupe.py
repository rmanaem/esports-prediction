import hashlib

#1
input_file_path = "../output/csv/lol-data-match-frames.csv"
output_file_path = "../output/csv/lol-data-match-frames-deduped.csv"

#2
completed_lines_hash = set()

#3
with open(input_file_path, "r") as inFile, open(output_file_path, "w") as outFile:
    #4
    for line in inFile:
        #5
        hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
        #6
        if hashValue not in completed_lines_hash:
            outFile.write(line)
            completed_lines_hash.add(hashValue)
    