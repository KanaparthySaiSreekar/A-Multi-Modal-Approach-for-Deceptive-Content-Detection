import requests


def fetch_sequence(chrom, start, end, genome='hg38'):
    base_url = f'https://api.genome.ucsc.edu/getData/sequence?genome={genome};chrom={chrom};start={start};end={end}'

    response = requests.get(base_url)
    if response.status_code == 200:
        sequence_data = response.json()
        sequence = sequence_data['dna']
        print(sequence_data)
        return sequence
    else:
        print(f"Failed to fetch sequence. Status code: {response.status_code}")
        return None


# print(fetch_sequence("chr17", 82272820, 82272980).upper())
import torch

# Load the file
pt_file = torch.load("C:/Users/vixha/Downloads/test-sample.pt", map_location=torch.device('cpu'))

# Print the head of the file
print((pt_file['sequence']))


