import can
import os
from tqdm import tqdm
import time
import sys

inputPath = './BlfFileToConvert/'
outputPath ='./BlfFileConverted/'

def FilterAlreadyConvertedFiles(inList, outList):
    set1= set(inList)
    set2= set(outList)
    return (set1 - set2)


def list_files(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(f"Directory '{dir}' does not exist. Please relaunch the script.")
        return 0
    else:
        try:
            # Get a list of all files in the directory
            files = os.listdir(dir)
            # TODO Implement extension test to only process BLF file
            file_names = [os.path.splitext(file)[0] for file in files]
        except FileNotFoundError:
            print(f"Directory '{dir}' not found.")
    return file_names

def ConvertFile(inFile):  
    # Get the size of the input file
    blf_file = inputPath+inFile+".blf"
    total_size = os.path.getsize(blf_file)
    descStr="Converting " + inFile + " in ASC file"
    outFile=outputPath+inFile+".asc"

    with open(blf_file, 'rb') as f_in:
        try:
            log_in = can.io.BLFReader(f_in)
        except Exception as e:
            raise Exception (blf_file + ": [ERROR] "+ str(e))

        # Set up the progress bar
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=descStr, colour='green') as pbar, open(outFile, 'w') as f_out:
            try:
                log_out = can.io.ASCWriter(f_out)
            except ValueError as e:
                raise e
            for msg in log_in:
                # Update the progress bar
                pbar.update(len(msg))
                log_out.on_message_received(msg)
            pbar.update(total_size)
            log_out.stop()

def main():
    try:
        outFiles = list_files(outputPath)
        infiles = list_files(inputPath)
        infiles=FilterAlreadyConvertedFiles(infiles, outFiles)
        res=0
        sTime=time.time()
        if not infiles:
            print ("All the files have been already converted !!!")
        else: 
            for file in infiles:
                try:
                    # Check file is a BLF file
                    ConvertFile(file)
                except Exception as e:
                    print (e)
        res=time.localtime(time.time()-sTime)
        # print("Time Elapsed: ", res.tm_sec)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    sys.exit(main())


