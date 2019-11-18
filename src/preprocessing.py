import os.path

import pandas as pd


def process_data(data_path, mean_sea_level_path, output_file_path, yearly_means_output_path):
    print(f"Pre-processing file: {data_path}")

    data = pd.read_csv(data_path)
    mean_sea_level_data = pd.read_csv(mean_sea_level_path)

    # if file exist then don't create a new one and read from it only
    if os.path.isfile(output_file_path):
        n_data = pd.read_csv(output_file_path)
        print(f"Read normalized data from {output_file_path}")
    else:
        n_data = data.copy()

        for i, row in n_data.iterrows():
            # FIXME: Small hack : to show the progress bar
            if i % 1000 == 0:
                print('\r ready: %.3f%%' % (i / len(n_data) * 100), end=" ")

            # main normalizing step, N2000
            # water_level - mean sea level data for that particular year
            n_data.iat[i, 5] = row['Water level (mm)'] - mean_sea_level_data.loc[mean_sea_level_data['Year'] ==
                                                                                 row['Year']].values[0][1]

        n_data = n_data.rename(columns={'Water level (mm)': 'water_level'})

        n_data.to_csv(output_file_path)

        print(f"\nWrote output to {output_file_path}")

    # finding the mean value of each year
    yearly_means = n_data["water_level"].groupby(n_data["Year"]).mean().dropna()

    with open(yearly_means_output_path, "w") as f:
        f.writelines(pd.Series.to_csv(yearly_means))

    return yearly_means


if __name__ == '__main__':
    data_path = r"../data/Kemi/Kemi.csv"
    mean_sea_level_path = r"../data/Kemi/Kemi_mw_n2000.csv"
    normalized_output_path = r"../data/Kemi/Kemi_normalized.csv"
    yearly_means_output_path = r"../data/Kemi/Kemi_yearly_means.csv"

    yearly_mean = process_data(data_path, mean_sea_level_path, normalized_output_path, yearly_means_output_path)

    print(yearly_mean)


from torchvision.models import vgg16