import argparse, os
from multiprocessing import Pool
from skimage.metrics import structural_similarity, peak_signal_noise_ratio
from skimage.io import imread
import pandas as pd

def is_image_format(filename):
    image_format = ['png','jpg','jpeg']
    filename_list = filename.split('.')
    if len(filename_list) == 1:
        return False 
    elif not filename_list[-1].lower() in image_format:
        return False
    return True

def find_images(root_directory, parent_directory=None):
    """find image in source directory"""
    images = []
    directory_images = []
    sub_directories = []
    search_directory = os.path.join(root_directory, parent_directory) if parent_directory is not None else root_directory
    for f in os.listdir(search_directory):
        path = os.path.join(parent_directory,f) if parent_directory is not None else f
        if os.path.isdir(os.path.join(root_directory,path)):
            sub_directories.append(path)
        elif is_image_format(f):
            directory_images.append(path)
    for directory in sub_directories:
        images += find_images(root_directory, directory)
    images += directory_images
    return images

def measure(data):
    """ measure PSNR and SSIM for each image """
    source, target, ssim_window, image = data
    source_image_path = os.path.join(source, image)
    target_image_path = os.path.join(target, image)
    if not os.path.exists(source_image_path):
        raise FileNotFoundError("Cannot find {}".format(source_image_path))
    if not os.path.exists(target_image_path):
        raise FileNotFoundError("Cannot find {}".format(target_image_path))
    source_image = imread(source_image_path)
    target_image = imread(target_image_path)
    if source_image.shape != target_image.shape:
        raise RuntimeError("{} and {} should have same image size".format(source_image_path, target_image_path))
    ssim = structural_similarity(source_image, target_image, win_size=ssim_window, multichannel=True)
    psnr = peak_signal_noise_ratio(source_image, target_image, data_range=255)
    return ssim, psnr

def measurement_pool(images, args):
    """ create pool for multithread processing """
    result = []
    with Pool(args.threads) as pool:
        data = [(args.source, args.target, args.ssim_window, img) for img in images]
        result = pool.map(measure, data)
    return zip(*result)

def main(args):
    images = find_images(args.source)
    ssims, psnrs  = measurement_pool(images, args)
    df = pd.DataFrame.from_dict({
        'image': images,
        'PSRN': psnrs,
        'SSIM': ssims,
    })
    if args.csv != '':
        csv_name = args.csv if '.csv' in args.csv else '{}.csv'.format(args.csv)
        df.to_csv(csv_name, index=False)
    if not args.mute:
        df['directory'] =  [os.path.dirname(image) for image in images]
        print("------------------------------------")
        print("Reconstruction Quality by directory")
        print("------------------------------------")
        print(df.groupby(['directory']).mean().to_string())
        print("------------------------------------")
        print("Average Reconstruction Quality")
        print("------------------------------------")
        print(df.mean().to_string())

def entry_point():
    parser = argparse.ArgumentParser()
    parser.add_argument("source",
        type=str,
        help="source directory to compare image",
        default="source")
    parser.add_argument('target',
        type=str,
        help='target directory to compare image',
        default='target'
    )
    parser.add_argument('--csv',
        default='',
        type=str,
        help="output path of csv file for future calculation (default: None)"
    )
    parser.add_argument('--threads',
        default=8,
        type=int,
        help="number of pararell threads (default: 40)"
    )
    parser.add_argument('--ssim-window',
        default=11,
        type=int,
        help="ssim windows size (odd integer only) (default: 11)"
    )
    parser.add_argument('--mute',
        action="store_true",
        default=False,
        help="Mute standard output"
    )
    args = parser.parse_args()
    main(args)

if __name__ =='__main__':
    entry_point()