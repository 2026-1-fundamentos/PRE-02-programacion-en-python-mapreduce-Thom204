import glob
import os.path
import time
import string




def copy_raw_files_to_input_folder(n):
    """Generate n copies of the raw files in the input folder"""
    if os.path.exists("files/input/"):
        for file in glob.glob("files/input/*"):
            os.remove(file)
    else:
        os.makedirs("files/input")


    for file in glob.glob("files/raw/*"):

        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        for i in range(1, n + 1):
            raw_filename_with_extension = os.path.basename(file)
            raw_filename_without_extension = os.path.splitext(raw_filename_with_extension)[0]
            new_filename = f"{raw_filename_without_extension}_{i}.txt"
            with open(f"files/input/{new_filename}", "w", encoding="utf-8") as f2:
                f2.write(text)


def load_input(input_directory):
    """Funcion load_input"""
    sequence = []
    files = glob.glob("files/input/*")
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                sequence.append(preprocess_line(line))
    
    return sequence



def preprocess_line(x):
    """Preprocess the line x"""
    res = x.lower()
    res = res.translate(str.maketrans("", "", string.punctuation))
    res = res.strip("\n")
    return res


def map_line(x):
    x= x.strip(".,()[]\t\n")
    return (x,1)

def mapper(sequence):
    bsec = []
    for ln in sequence:
        words = ln.strip(" ").split(" ")
        bsec.extend([map_line(word) for word in words])
    return bsec


def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    return sorted(sequence)



def compute_sum_by_group(group):
    pass

def reducer(sequence):
    """Reducer"""
    result = []
    for key, value in sequence:
        if result and result[-1][0] == key:
            result[-1] = (key, result[-1][1] + value)
        else:
            result.append((key, value))
        
    return result
            


def create_directory(directory):
    """Create Output Directory"""
    if os.path.exists(directory):
        for file in glob.glob(f"{directory}/*"):
            os.remove(file)
    else:
        os.makedirs(directory)


def save_output(output_directory, sequence):
    """Save Output"""
    with open(f'{output_directory}/part-00000', "w", encoding="utf-8") as f:
        f.writelines([f'{k}\t{v}\n' for k,v in sequence])


def create_marker(output_directory):
    """Create Marker"""
    # Crea el archivo _SUCCESS en files/output
    with open(f'{output_directory}/_SUCCESS', "w", encoding="utf-8") as f:
        f.write("")


def run_job(input_directory, output_directory):
    """Job"""
    sequence = load_input(input_directory)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory)


if __name__ == "__main__":

    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(
        "files/input",
        "files/output",
    )

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
