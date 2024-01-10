import argparse, tempfile, shutil
from utils import *
from dict import create_dict

def read_args():
    parser = argparse.ArgumentParser(description='Process JSON data.')
    parser.add_argument('-data_path')
    parser.add_argument('-output_path')
    return parser.parse_args()

def main():
    args = read_args()
    data_path = args.data_path
    output_path = f"{args.output_path}/cross-lang"

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for language, projects in CROSS_LANGAUGE_PROJECTS.items():

        tmp_out_dir = tempfile.mkdtemp(prefix='language.', dir=output_path)
        sub_dirs = []
        for i in range(9):
            tmp_sub_dir = tempfile.mkdtemp(prefix=f'sub_{i}.', dir=tmp_out_dir)
            sub_dirs.append(tmp_sub_dir)

        for project in projects:

            path = f"{data_path}/{project}"
            commits_path, features_path = os.listdir(path)
            commits_path, features_path = f"{path}/{commits_path}", f"{path}/{features_path}"
            
            commit_files = os.listdir(commits_path)
            feature_files = os.listdir(features_path)

            # Filter out file
            files_to_get = get_list_files(project)

            index = 0
            for file in feature_files:
                if file in files_to_get:
                    file_path = f"{features_path}/{file}"
                    shutil.copy(file_path, sub_dirs[files_to_get.index(file)])
                    index += 1

            for file in commit_files:
                if file in files_to_get:
                    file_path = f"{commits_path}/{file}"
                    shutil.copy(file_path, sub_dirs[files_to_get.index(file)])
                    index += 1

            # Combine
            for index, dir in enumerate(sub_dirs):
                files = os.listdir(dir)
                
                if index in range(6):
                    language_commit = combine_commit(dir, files)

                    if index == 2:
                        save_name = f'{language}/commits/{language}_part_1_part_4_train_dict.pkl'
                        dict = create_dict(language_commit[1], language_commit[2])

                        save_path = f"{output_path}/{save_name}"
                        if not os.path.exists(os.path.dirname(save_path)):
                            os.makedirs(os.path.dirname(save_path))
                        with open(save_path, 'wb') as file:
                            pickle.dump(dict, file)

                    save_name = get_save_name(index, language)
                    save_path = f"{output_path}/{save_name}"
                    if not os.path.exists(os.path.dirname(save_path)):
                        os.makedirs(os.path.dirname(save_path))
                    with open(save_path, 'wb') as file:
                        pickle.dump(language_commit, file)
                else:
                    language_feature = combine_feature(dir, files)

                    save_name = get_save_name(index, language)
                    save_path = f"{output_path}/{save_name}"
                    if not os.path.exists(os.path.dirname(save_path)):
                        os.makedirs(os.path.dirname(save_path))
                    language_feature.to_csv(save_path, index=False)
                
        shutil.rmtree(tmp_out_dir)

if __name__ == "__main__":
    main()