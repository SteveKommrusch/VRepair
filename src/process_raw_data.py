import argparse
import math
import random
import sys
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Generate data suitble for seq2seq training.')
parser.add_argument('-data_dir', action='store',
                    dest='data_dir', help='Path to all raw data')
parser.add_argument('-max_src_length', action='store',
                    dest='max_src_length', type=int, help='Maximum src token length')
parser.add_argument('-max_tgt_length', action='store',
                    dest='max_tgt_length', type=int, help='Maximum tgt token length')
parser.add_argument('--split_range', action='store', nargs='+',
                    dest='split_range', type=float,
                    help='train/valid/test data range, must sum up to 100')
parser.add_argument('--fixed_split', action='store_true', dest='fixed_split',
                    help='If the valid/test data size is fixed, mutually exclusive with split_range')
parser.add_argument('--commits', action='store_true', dest='commits',
                    help='Process BugFixTokenPairs_commits data (security vulnerabilities)')
parser.add_argument('--fixed_split_size', action='store', type=int,
                    dest='fixed_split_size',
                    help='If fixed_split, the size of valid/test data')
parser.add_argument('--output_dir', action='store', dest='output_dir',
                    default='./', help='Output directory')


def read_all_data(data_dir,commits):
    src_list = []
    tgt_list = []
    # Read all data as they are.
    if commits:
        src_filename = f'BugFixTokenPairs_commits.src.txt'
        tgt_filename = f'BugFixTokenPairs_commits.tgt.txt'

        with open(data_dir / src_filename) as f:
            src_list.extend(f.read().splitlines())
        with open(data_dir / tgt_filename) as f:
            tgt_list.extend(f.read().splitlines())
    else:
        for year in ('2017', '2018'):
            for month in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'):
                src_filename = f'BugFixNoDup_{year}_{month}.src.txt'
                tgt_filename = f'BugFixNoDup_{year}_{month}.tgt.txt'

                with open(data_dir / src_filename) as f:
                    src_list.extend(f.read().splitlines())
                with open(data_dir / tgt_filename) as f:
                    tgt_list.extend(f.read().splitlines())

    # Remove instances where the src or tgt is whitespace only.
    src_nonempty_list = []
    tgt_nonempty_list = []
    counts={}
    for src in src_list:
        cwe=src.split()[0]
        if cwe in counts:
            counts[cwe]+=1
        else:
            counts[cwe]=1
    for src, tgt in zip(src_list, tgt_list):
        if src.strip() and tgt.strip():
            if commits:
                cwe=src.split()[0]
                # Include CWE numbers for those with over 20 samples
                # (these account for over 90% of cases in TokenPairs_commits
                if counts[cwe] > 20:
                    src_nonempty_list.append(src)
                else:
                    src_nonempty_list.append(src.replace(cwe,'CWE-000'))
                tgt_nonempty_list.append(tgt)
            else:
                # Add null CWE value to this pretraining data
                src_nonempty_list.append("CWE-000 "+src)
                tgt_nonempty_list.append(tgt)
    return src_nonempty_list, tgt_nonempty_list


def remove_duplicate(src_list, tgt_list):
    src_unique_list = []
    tgt_unique_list = []
    unique_pairs = set()

    for src, tgt in zip(src_list, tgt_list):
        if (src, tgt) not in unique_pairs:
            unique_pairs.add((src, tgt))
            src_unique_list.append(src)
            tgt_unique_list.append(tgt)

    return src_unique_list, tgt_unique_list


def remove_long_sequence(src_list, tgt_list, max_src_length, max_tgt_length):
    src_suitable_list = []
    tgt_suitable_list = []

    for src, tgt in zip(src_list, tgt_list):
        if len(src.split(' ')) <= max_src_length and len(tgt.split(' ')) <= max_tgt_length:
            src_suitable_list.append(src)
            tgt_suitable_list.append(tgt)

    return src_suitable_list, tgt_suitable_list


def split_train_val_test(src_list, tgt_list, fixed_split, split_range,
                         fixed_split_size):
    src_tgt_pairs = list(zip(src_list, tgt_list))
    random.shuffle(src_tgt_pairs)
    src_list, tgt_list = zip(*src_tgt_pairs)

    list_count = len(src_list)
    if fixed_split:
        train_index = max(0, list_count-fixed_split_size-fixed_split_size)
        validation_index = train_index + fixed_split_size
    else:
        train_index = math.floor((split_range[0] / 100) * list_count)
        validation_index = math.floor((split_range[1] / 100) * list_count)
        validation_index += train_index

    train_src_list = src_list[:train_index]
    train_tgt_list = tgt_list[:train_index]
    valid_src_list = src_list[train_index:validation_index]
    valid_tgt_list = tgt_list[train_index:validation_index]
    test_src_list = src_list[validation_index:list_count]
    test_tgt_list = tgt_list[validation_index:list_count]

    return (train_src_list, train_tgt_list,
            valid_src_list, valid_tgt_list,
            test_src_list, test_tgt_list)


def main(argv):
    args = parser.parse_args(argv)

    assert(bool(args.split_range) != args.fixed_split)

    if args.split_range:
        assert(len(args.split_range) == 3)
        assert(sum(args.split_range) == 100)

    data_dir = Path(args.data_dir).resolve()
    src_list, tgt_list = read_all_data(data_dir,args.commits)
    src_list, tgt_list = remove_duplicate(src_list, tgt_list)
    src_list, tgt_list = remove_long_sequence(
        src_list, tgt_list, args.max_src_length, args.max_tgt_length)
    (train_src_list, train_tgt_list, valid_src_list, valid_tgt_list,
     test_src_list, test_tgt_list) = split_train_val_test(
        src_list, tgt_list, args.fixed_split, args.split_range,
        args.fixed_split_size)

    if args.commits:
        train_src_filename = 'BugFixCommits_train_src.txt'
        train_tgt_filename = 'BugFixCommits_train_tgt.txt'
        valid_src_filename = 'BugFixCommits_valid_src.txt'
        valid_tgt_filename = 'BugFixCommits_valid_tgt.txt'
        test_src_filename = 'BugFixCommits_test_src.txt'
        test_tgt_filename = 'BugFixCommits_test_tgt.txt'
    else:
        train_src_filename = 'BugFix_train_src.txt'
        train_tgt_filename = 'BugFix_train_tgt.txt'
        valid_src_filename = 'BugFix_valid_src.txt'
        valid_tgt_filename = 'BugFix_valid_tgt.txt'
        test_src_filename = 'BugFix_test_src.txt'
        test_tgt_filename = 'BugFix_test_tgt.txt'

    output_dir = Path(args.output_dir).resolve()
    with open(output_dir / train_src_filename, encoding='utf-8', mode='w') as f:
        f.write('\n'.join(train_src_list) + '\n')
    with open(output_dir / train_tgt_filename, encoding='utf-8', mode='w') as f:
        f.write('\n'.join(train_tgt_list) + '\n')
    with open(output_dir / valid_src_filename, encoding='utf-8', mode='w') as f:
        f.write('\n'.join(valid_src_list) + '\n')
    with open(output_dir / valid_tgt_filename, encoding='utf-8', mode='w') as f:
        f.write('\n'.join(valid_tgt_list) + '\n')
    with open(output_dir / test_src_filename, encoding='utf-8', mode='w') as f:
        f.write('\n'.join(test_src_list) + '\n')
    with open(output_dir / test_tgt_filename, encoding='utf-8', mode='w') as f:
        f.write('\n'.join(test_tgt_list) + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])
